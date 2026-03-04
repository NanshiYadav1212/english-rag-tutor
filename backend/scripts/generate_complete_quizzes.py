import json

# Comprehensive quiz data for all 10 lessons
quizzes_data = {
    "quizzes": [
        {
            "lesson_slug": "basics-of-english-grammar",
            "quiz_types": {
                "multiple_choice": {
                    "questions": [
                        {"question_id": 1, "question": "Which is the most essential component of a sentence?", "options": ["Adjective", "Subject and Verb", "Punctuation", "Preposition"], "correct_answer": "Subject and Verb", "marks": 1},
                        {"question_id": 2, "question": "What is the primary purpose of punctuation?", "options": ["Make writing pretty", "Clarify meaning", "Replace words", "Add length"], "correct_answer": "Clarify meaning", "marks": 1},
                        {"question_id": 3, "question": "In 'The cat sat on the mat,' what is 'mat'?", "options": ["Subject", "Verb", "Object of preposition", "Adjective"], "correct_answer": "Object of preposition", "marks": 1},
                        {"question_id": 4, "question": "Which word order pattern does English follow?", "options": ["VSO", "SVO", "OSV", "VOS"], "correct_answer": "SVO", "marks": 1},
                        {"question_id": 5, "question": "What does 'agreement' in grammar mean?", "options": ["Using same word twice", "Words matching in number", "Putting words in order", "Using punctuation"], "correct_answer": "Words matching in number", "marks": 1},
                        {"question_id": 6, "question": "Which sentence has correct structure?", "options": ["Running quickly to store", "She runs to store", "Store to runs she", "To runs store quickly"], "correct_answer": "She runs to store", "marks": 1},
                        {"question_id": 7, "question": "In 'The blue bicycle', what is 'blue'?", "options": ["Noun", "Verb", "Adjective", "Adverb"], "correct_answer": "Adjective", "marks": 1},
                        {"question_id": 8, "question": "What is a predicate?", "options": ["Subject of sentence", "What subject does", "Punctuation mark", "First word"], "correct_answer": "What subject does", "marks": 1},
                        {"question_id": 9, "question": "Which is a complete sentence?", "options": ["Walking in park", "The park is beautiful", "Because it was cold", "Running quickly"], "correct_answer": "The park is beautiful", "marks": 1},
                        {"question_id": 10, "question": "What type of phrase is 'on the table'?", "options": ["Noun phrase", "Verb phrase", "Prepositional phrase", "Adjective phrase"], "correct_answer": "Prepositional phrase", "marks": 1}
                    ]
                },
                "true_false": {
                    "questions": [
                        {"question_id": 1, "question": "Every sentence must have both a subject and a verb.", "correct_answer": "True", "marks": 1},
                        {"question_id": 2, "question": "Adjectives are used to describe verbs.", "correct_answer": "False", "marks": 1},
                        {"question_id": 3, "question": "A prepositional phrase always shows location.", "correct_answer": "False", "marks": 1},
                        {"question_id": 4, "question": "Word order can change the meaning of a sentence.", "correct_answer": "True", "marks": 1},
                        {"question_id": 5, "question": "Punctuation is not important in grammar.", "correct_answer": "False", "marks": 1},
                        {"question_id": 6, "question": "A phrase always contains a verb.", "correct_answer": "False", "marks": 1},
                        {"question_id": 7, "question": "Subject-verb agreement means verb matches subject's number.", "correct_answer": "True", "marks": 1},
                        {"question_id": 8, "question": "An object always comes before the verb in English.", "correct_answer": "False", "marks": 1},
                        {"question_id": 9, "question": "Grammar helps ensure your message is understood.", "correct_answer": "True", "marks": 1},
                        {"question_id": 10, "question": "Punctuation can never change the meaning.", "correct_answer": "False", "marks": 1}
                    ]
                },
                "fill_in_blanks": {
                    "questions": [
                        {"question_id": 1, "question": "A sentence must have a _____ and a verb.", "correct_answer": "subject", "marks": 1},
                        {"question_id": 2, "question": "_____ words describe or modify nouns.", "correct_answer": "Adjectives", "marks": 1},
                        {"question_id": 3, "question": "The _____ is the action word in a sentence.", "correct_answer": "verb", "marks": 1},
                        {"question_id": 4, "question": "In 'He runs quickly,' 'quickly' is an _____.", "correct_answer": "adverb", "marks": 1},
                        {"question_id": 5, "question": "A _____ phrase begins with a preposition.", "correct_answer": "prepositional", "marks": 1},
                        {"question_id": 6, "question": "The _____ of a sentence tells what the subject does.", "correct_answer": "predicate", "marks": 1},
                        {"question_id": 7, "question": "Subject-verb _____ means verb matches subject's number.", "correct_answer": "agreement", "marks": 1},
                        {"question_id": 8, "question": "The _____ 'the' is used for specific nouns.", "correct_answer": "article", "marks": 1},
                        {"question_id": 9, "question": "A _____ expresses emotion like 'Oh!' or 'Wow!'", "correct_answer": "interjection", "marks": 1},
                        {"question_id": 10, "question": "The basic structure of English is _____.", "correct_answer": "Subject-Verb-Object", "marks": 1}
                    ]
                },
                "sentence_correction": {
                    "questions": [
                        {"question_id": 1, "question": "Correct: 'She go to school every day.'", "correct_answer": "go → goes", "marks": 1},
                        {"question_id": 2, "question": "Correct: 'The book are on the table.'", "correct_answer": "are → is", "marks": 1},
                        {"question_id": 3, "question": "Correct: 'I seen the movie yesterday.'", "correct_answer": "seen → saw", "marks": 1},
                        {"question_id": 4, "question": "Correct: 'They doesn't like pizza.'", "correct_answer": "doesn't → don't", "marks": 1},
                        {"question_id": 5, "question": "Correct: 'The students studies hard.'", "correct_answer": "studies → study", "marks": 1},
                        {"question_id": 6, "question": "Correct: 'He walk to the store.'", "correct_answer": "walk → walks", "marks": 1},
                        {"question_id": 7, "question": "Correct: 'The cats is sleeping.'", "correct_answer": "is → are", "marks": 1},
                        {"question_id": 8, "question": "Correct: 'I goes to the gym.'", "correct_answer": "goes → go", "marks": 1},
                        {"question_id": 9, "question": "Correct: 'She have a new car.'", "correct_answer": "have → has", "marks": 1},
                        {"question_id": 10, "question": "Correct: 'We runs in the morning.'", "correct_answer": "runs → run", "marks": 1}
                    ]
                },
                "short_answer": {
                    "questions": [
                        {"question_id": 1, "question": "What is the difference between subject and object?", "correct_answer": "Subject performs action; object receives it", "marks": 1},
                        {"question_id": 2, "question": "Why does word order matter in English?", "correct_answer": "It determines meaning and who does what to whom", "marks": 1},
                        {"question_id": 3, "question": "What is a prepositional phrase? Give an example.", "correct_answer": "Phrase with preposition showing relationships; e.g., 'in the house'", "marks": 1},
                        {"question_id": 4, "question": "Define grammar and its importance.", "correct_answer": "System of language rules ensuring clear communication", "marks": 1},
                        {"question_id": 5, "question": "What is the difference between clause and phrase?", "correct_answer": "Clause has subject and verb; phrase does not", "marks": 1},
                        {"question_id": 6, "question": "Give an example of correct subject-verb agreement.", "correct_answer": "The cat is sleeping / The cats are sleeping", "marks": 1},
                        {"question_id": 7, "question": "What are the main parts of a simple sentence?", "correct_answer": "Subject and predicate (verb)", "marks": 1},
                        {"question_id": 8, "question": "Explain the importance of punctuation.", "correct_answer": "Punctuation clarifies meaning and structure", "marks": 1},
                        {"question_id": 9, "question": "What is an independent clause?", "correct_answer": "Clause with subject and verb that expresses complete thought", "marks": 1},
                        {"question_id": 10, "question": "How does grammar affect professionalism?", "correct_answer": "Proper grammar shows competence and builds credibility", "marks": 1}
                    ]
                }
            }
        },
        {
            "lesson_slug": "parts-of-speech",
            "quiz_types": {
                "multiple_choice": {
                    "questions": [
                        {"question_id": 1, "question": "How many parts of speech are there in English?", "options": ["7", "8", "9", "10"], "correct_answer": "9", "marks": 1},
                        {"question_id": 2, "question": "Which part of speech names people, places, or things?", "options": ["Verb", "Noun", "Adjective", "Adverb"], "correct_answer": "Noun", "marks": 1},
                        {"question_id": 3, "question": "What does a pronoun replace?", "options": ["Verbs", "Adjectives", "Nouns", "Prepositions"], "correct_answer": "Nouns", "marks": 1},
                        {"question_id": 4, "question": "Which word is a verb in this sentence: 'She quickly ran to the store'?", "options": ["She", "quickly", "ran", "store"], "correct_answer": "ran", "marks": 1},
                        {"question_id": 5, "question": "Identify the adjective: 'The beautiful flower bloomed today.'", "options": ["beautiful", "flower", "bloomed", "today"], "correct_answer": "beautiful", "marks": 1},
                        {"question_id": 6, "question": "Which is a preposition?", "options": ["quickly", "happy", "over", "is"], "correct_answer": "over", "marks": 1},
                        {"question_id": 7, "question": "What do adverbs typically modify?", "options": ["Nouns", "Pronouns", "Verbs or adjectives", "Prepositions"], "correct_answer": "Verbs or adjectives", "marks": 1},
                        {"question_id": 8, "question": "Which word is a conjunction?", "options": ["run", "and", "beautiful", "over"], "correct_answer": "and", "marks": 1},
                        {"question_id": 9, "question": "Identify the interjection: 'Oh! What a surprise!'", "options": ["What", "surprise", "Oh", "a"], "correct_answer": "Oh", "marks": 1},
                        {"question_id": 10, "question": "What is the definite article?", "options": ["a", "an", "the", "this"], "correct_answer": "the", "marks": 1}
                    ]
                },
                "true_false": {
                    "questions": [
                        {"question_id": 1, "question": "Nouns are the only parts of speech that can be subjects.", "correct_answer": "False", "marks": 1},
                        {"question_id": 2, "question": "Pronouns replace nouns to avoid repetition.", "correct_answer": "True", "marks": 1},
                        {"question_id": 3, "question": "All verbs show action.", "correct_answer": "False", "marks": 1},
                        {"question_id": 4, "question": "Adjectives describe verbs.", "correct_answer": "False", "marks": 1},
                        {"question_id": 5, "question": "Adverbs often end in -ly.", "correct_answer": "True", "marks": 1},
                        {"question_id": 6, "question": "Prepositions show relationships between words.", "correct_answer": "True", "marks": 1},
                        {"question_id": 7, "question": "Conjunctions connect words, phrases, or clauses.", "correct_answer": "True", "marks": 1},
                        {"question_id": 8, "question": "Interjections are always important to the sentence.", "correct_answer": "False", "marks": 1},
                        {"question_id": 9, "question": "'Very' is an adverb.", "correct_answer": "True", "marks": 1},
                        {"question_id": 10, "question": "Articles modify verbs.", "correct_answer": "False", "marks": 1}
                    ]
                },
                "fill_in_blanks": {
                    "questions": [
                        {"question_id": 1, "question": "A _____ names a person, place, thing, or idea.", "correct_answer": "noun", "marks": 1},
                        {"question_id": 2, "question": "A _____ replaces a noun to avoid repetition.", "correct_answer": "pronoun", "marks": 1},
                        {"question_id": 3, "question": "A _____ is an action word.", "correct_answer": "verb", "marks": 1},
                        {"question_id": 4, "question": "An _____ describes a noun or pronoun.", "correct_answer": "adjective", "marks": 1},
                        {"question_id": 5, "question": "An _____ modifies verbs or adjectives.", "correct_answer": "adverb", "marks": 1},
                        {"question_id": 6, "question": "A _____ shows relationships between words.", "correct_answer": "preposition", "marks": 1},
                        {"question_id": 7, "question": "A _____ connects words, phrases, or clauses.", "correct_answer": "conjunction", "marks": 1},
                        {"question_id": 8, "question": "An _____ expresses emotion.", "correct_answer": "interjection", "marks": 1},
                        {"question_id": 9, "question": "The _____ 'the' is the definite article.", "correct_answer": "definite",
