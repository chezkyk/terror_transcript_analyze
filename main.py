import json
import csv
import re

NUMBER_OF_SCRIPT_FILES = 3
NUMBER_OF_CSV_FILES = 100


def return_list_of_paths():
    transcript_list = []
    for i in range(NUMBER_OF_SCRIPT_FILES):
        transcript_name = f"C:\\Users\\Admin\\Downloads\\transcript_{i + 1}.txt"
        transcript_list.append(transcript_name)
    return transcript_list


def add_content_of_text_file(list_of_text_files_paths):
    content_of_all_text_files = []
    for path in list_of_text_files_paths:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
            content_of_all_text_files.append(content)
    return content_of_all_text_files


list_of_text_files_paths = return_list_of_paths()
list_of_text_files_contents = add_content_of_text_file(list_of_text_files_paths)


# print(list_of_text_files_contents)
# print(list_of_text_files_contents[0])
# print(list_of_text_files_contents[1])
# print(list_of_text_files_contents[2])
# print(len(list_of_text_files_contents))


def return_dict_of_known_words(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        known_words_dict = json.loads(content)
    return known_words_dict


path_of_known_words_file = "C:\\Users\\Admin\\Downloads\\known_words.json"
dict_of_known_words = return_dict_of_known_words(path_of_known_words_file)


# print(return_dict_of_known_words(path_of_known_words_file))


def search_if_word_is_in_known_words(word):
    the_word = None
    path = "C:\\Users\\Admin\\Downloads\\known_words.json"
    dict_of_known_words = return_dict_of_known_words(path)
    # חיפוש במילון 'decrypted_meanings'
    if word in dict_of_known_words.get("decrypted_meanings", {}):
        the_word = dict_of_known_words["decrypted_meanings"][word]

    # חיפוש במילון 'additional_context'
    if the_word is None:  # רק אם לא נמצא עד כה
        additional_context = dict_of_known_words.get("additional_context", {})
        participants = additional_context.get("participants", {})

        # חיפוש במילון 'participants'
        if word in participants:
            the_word = participants[word]


    return the_word
# print(search_if_word_is_in_known_words("הפנתר"))





def add_context_score_to_dict(path):
    with open(path, 'r', encoding='utf-8') as file:
        context_scores_dict = {}
        content = file.readlines()
        for line in content:
            line = line.strip()
            word, score = line.split(":")
            word = word.strip()
            score = float(score.strip())
            context_scores_dict[word] = score
    return context_scores_dict


path_of_context_scores_file = "C:\\Users\\Admin\\Downloads\\context_score.txt"
dict_of_context_scores = add_context_score_to_dict(path_of_context_scores_file)


# print(add_context_score_to_dict(path_of_context_scores_file))

def search_if_word_is_a_code_word(word):
    limit_code_word = 0.25
    for known_word, score in dict_of_context_scores.items():
        if known_word == word and score <= limit_code_word:
            return True
    return False


word_to_search_in_context_score_file = "ניפגש"
bool_anas_word_is_a_code_word = search_if_word_is_a_code_word(word_to_search_in_context_score_file)


# print(bool_anas_word_is_a_code_word)

def search_a_word_in_known_words_json(word):
    for known_word, score in dict_of_known_words.items():
        for context_word, context_score in score.items():
            if context_word == word:
                return context_score


word_to_search_in_json_file = "צהובה"


# print(search_a_word_in_known_words_json(word_to_search_in_json_file))

def return_content_of_csv_file(path):
    list_of_actual_word = []
    list_of_potential_meaning = []
    list_of_frequency = []
    list_of_context_score = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        headers_list = next(csvreader)
        for row in csvreader:
            list_of_actual_word.append(row[headers_list.index("Actual Word")])
            list_of_potential_meaning.append(row[headers_list.index("Potential Meaning")])
            list_of_frequency.append(row[headers_list.index("Frequency")])
            list_of_context_score.append(row[headers_list.index("Context Score")])

            all_lists = list(
                zip(list_of_actual_word, list_of_potential_meaning, list_of_frequency, list_of_context_score))
    return all_lists


# path_of_csv_file = "C:\\Users\\Admin\\Downloads\\file_1.csv"
# content_of_csv_file = return_content_of_csv_file(path_of_csv_file)
# print(return_content_of_csv_file(path_of_csv_file))


def return_a_list_of_all_csv_files():
    list_of_csv_files = []
    for i in range(1, NUMBER_OF_CSV_FILES + 1):
        current_csv_file_name = f"C:\\Users\\Admin\\Downloads\\csv_files\\file_{i}.csv"
        current_list = return_content_of_csv_file(current_csv_file_name)
        list_of_csv_files.append(current_list)
    return list_of_csv_files


list_of_csv_files = return_a_list_of_all_csv_files()


# print(list_of_csv_files)
def search_a_word_in_csv_file(word):
    mathing_words_list = []
    for csv_file_content in list_of_csv_files:
        for actual_word, potential_meaning, frequency, context_score in csv_file_content:
            if actual_word == word:
                mathing_words_list.append((actual_word, potential_meaning, frequency, context_score))
    return mathing_words_list


word_to_search_in_csv_file = "פיסטוק"
list_of_matching_words = search_a_word_in_csv_file(word_to_search_in_csv_file)


# print(list_of_matching_words)
# print(len(list_of_matching_words))

def return_a_transcript_list(transcript_number):
    patterns = [
        r"פריט א׳", r"פריט ב׳", r"פריט ג׳", r"פריט ד׳", r"פריט ה׳", r"סוף תצפית פריט", r"סוף תמליל", r"\d{2}:\d{2}"
    ]
    text = list_of_text_files_contents[transcript_number]
    for pattern in patterns:
        text = re.sub(pattern, lambda x: x.group(0).replace(" ", "_"), text)

    words = re.findall(r'\b[\w׳]+|\d{2}:\d{2}|\S', text)

    words = [word.replace("_", " ") for word in words]

    return words

# transcript_number = 0
# transcript_list = return_a_transcript_list(transcript_number)
# print(transcript_list)

def return_highest_chance_word(word):
    val = None
    list_of_words = search_a_word_in_csv_file(word)
    max_chance_value = -float('inf')
    max_chance_word = None
    for actual_word, potential_meaning, frequency, context_score in list_of_words:
        chance_word = float(frequency) * float(context_score)
        if chance_word > max_chance_value:
            max_chance_value = chance_word
            max_chance_word = (actual_word, potential_meaning, frequency, context_score)
            val = max_chance_word[1]
    return val
# word_to_analyze = "צהובה"
# highest_chance_word = return_highest_chance_word(word_to_analyze)
# print(highest_chance_word)

def analyze_transcript_words(transcript_number, word_witaout_start=None):
    list_of_words = return_a_transcript_list(transcript_number)
    for i in range(0, len(list_of_words)):
        all_word = list_of_words[i]

        word_witaout_start = all_word[1:]
        known_word1 = search_if_word_is_in_known_words(all_word)
        known_word2 = search_if_word_is_in_known_words(word_witaout_start)
        if known_word1 != None:
            if type(known_word1) == list:
                list_of_words[i] = "/".join(known_word1)
        elif known_word2 != None:
            if type(known_word2) == list:
                list_of_words[i] = "/".join(known_word2)
        else:
            ans_all_word = search_if_word_is_a_code_word(all_word)
            ans_word_witaout_start = search_if_word_is_a_code_word(word_witaout_start)
            if ans_all_word or ans_word_witaout_start:
                # להוסיף לוגיקה במקרה שהמילה לא מופיעה בג''יסון אבל היא מילת קוד
                ans1 = return_highest_chance_word(all_word)
                ans2 = return_highest_chance_word(word_witaout_start)
                if ans1:
                    list_of_words[i] = ans1
                    continue
                elif ans2:
                    list_of_words[i] = ans2
                    continue
                else:
                    list_of_words[i] = list_of_words[i]
            else:
                continue
    return list_of_words


def start_program():
    for i in range(NUMBER_OF_SCRIPT_FILES):
        sentence_list = analyze_transcript_words(i)

        sentence_list = [str(item) if not isinstance(item, str) else item for item in sentence_list]

        sentence = " ".join(sentence_list).replace(" ,", ",").replace(" .", ".")

        print(sentence)


start_program()
