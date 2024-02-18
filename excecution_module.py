import pandas as pd
import concurrent.futures
from openai import OpenAI
# import tkinter
# from tkinter import messagebox

# Replace this with your actual OpenAI API key
def start_excussion():
    api_key = "MY_API_KEY"

    def get_language_name(locale_code):
        # Mapping between locale codes and language names
        language_names = {
            'en_US': 'English (United States)',
            'en_GB': 'English (United Kingdom)',
            'fr_FR': 'French (France)',
            'it_IT': 'Italian (Italy)',
            # Add more mappings as needed
        }
        
        return language_names.get(locale_code, None)

    # Function to call OpenAI and generate informal version
    def callOpenAI(prompt):
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You will be provided with the content of a string and the locale. Your task is to make sure that the content of the string is in the language locale given following the below instructions. Also you need to provide a seperate short 1 or 2 sentence explanation for your changes and if no changes are made, just provide (OK) in comment. Please use %% before starting comment. Must include both evaluated option and comment in the response. The response should be like this, {evaluated option}%%{comment}."},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content

    # Load your Excel file
    file_path = 'uploads/excel_file.xlsx'
    df = pd.read_excel(file_path)

    # Function to process a batch of rows concurrently
    def process_batch(rows):
        for index, row in rows.iterrows():
            formal_text = get_language_name(row['locale'])
            source_text = row['content']
            prompt = f"""The locale is: '{formal_text}' \n The content of string is: '{source_text}'.
    You will be provided with content and language locale and You have to evaluate provided content and answer only one word from these options: Correct, Inorrect, Mixed, N/A. Decide option according to these detail:
        • Correct - all text in in content is in the expected language locale
        • Incorrect - all text in content is consistently in a language, but not the provided language locale
        • Mixed - the text in content contains a mix of languages (i.e. contains some text in the expected language, but not all of it). Brand names in a different language then the expected language locale fall into this category
        • N/A - Non-linguistic text at all (only codes and numbers)

    Some additional details:
        • If the language in Content is correct but there's any kind of error (spelling, grammar, etc.), you can consider the entry as correct for the purpose of this task.
        • If the language variety of the entry in content differs from the provied language locale, for instance es-MX word for es-ES target, we can consider the entry in content as correct as well, because the word would still be in Spanish, regardless of the variety.
        • If an entry in content has words and also numbers or special characters, you should consider only the words/phrase and evaluate it accordingly. 
            ◦ E.g. analysing this string ‘%20%20WC-Sitze’ in de-DE, evaluate it as ‘Correct’ since “Sitze” is still a German word, 
            ◦ But evaluate this string ‘19OLY202’ as N/A since it’s made only by codes/numbers.
        • If a cell only have numbers or non-linguistic text, then the evaluation would be N/A. 
        • If a cell have linguistic text with numbers or special characters with it (%20%20WC-Sitze), it should be evaluated as Correct if it’s in the desired language, and Incorrect if it’s not the desired language
        • For email and addresses:
            ◦ if in the cell there is only an email address or a postal address, then the cell should be evaluated N/A
            ◦ if the email address is in the middle of a sentence, then it should be evaluated as Correct / Incorrect / Mixed based on correctness of the cell content.
        • Numbers with units of measure or currency signs are to be considered correct if in the appropriate language, even if the unit of measure is not the usual for that language. For example, in de-DE, Preis: 34,99 € and Preis: $34.99 would be marked as correct for this exercise.
        • Prices / unit of measures only (34,99 €) should be marked as N/A, but if it has linguistic text  around it, then it should be Correct / Incorrect / Mixed based on the language being evaluated.
            ◦ We do not need to verify number or currency formatting at this stage, even if they are unusual in the target language. In the example provided: “Preis: 34,99 €” is Correct for de-DE, but “34,99 €” should be N/A
        • If the URLs are completely alone, then it’s ‘N/A’. If it’s embedded within text, evaluate  that on the language of the surrounding text.
        • If there is a name of an actual person, or company, in an entry, and the name is in another language, the asset should be flagged as “Mixed”. 
            ◦ For example, if the expected  language is Spanish, and the sentence is: “Sophie Dahl, la renombrada  autora de cuentos infantiles, dará una charla en la Feria del Libro”.  The name “Sophie” is technically in another language, because in Spanish  the name would be “Sofía” so it’s marked as “Mixed”

    """

            # Call OpenAI to generate informal version
            informal_text = callOpenAI(prompt)
            # Find the index of the delimiter
            delimiter_index = informal_text.find("%%")

    # Slice the sentence into two parts
            translation = informal_text[:delimiter_index]
            # Check if translation has single or double quotations and remove them
            if translation.startswith("'") and translation.endswith("'"):
                translation = translation[1:-1]
            elif translation.startswith('"') and translation.endswith('"'):
                translation = translation[1:-1]

            comment = informal_text[delimiter_index + 2:]

            # Display evaluation and comment in the log

            print('Row', index , ' Done')

            # print("Comment:", comment)
            df.at[index, 'Evaluation'] = translation
            df.at[index, 'Comments'] = comment


    # Split the DataFrame into batches
    batch_size = 2
    batches = [df[i:i+batch_size] for i in range(0, len(df), batch_size)]

    # Process each batch concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_batch, batches)

    # Convert the 'Comment' column to string
    df['Comments'] = df['Comments'].astype(str)

    # Save the updated DataFrame to a new Excel file
    df.to_excel('uploads/downloads/updated_excel_file.xlsx', index=False)
    print('File Created Successfully!')


