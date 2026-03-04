import json

# Complete quiz data for remaining 4 lessons
remaining_quizzes = []

# Lesson 7: Sentence Structure
lesson_7 = {
    "lesson_slug": "sentence-structure",
    "lesson_title": "Sentence Structure",
    "quiz_types": {
        "multiple_choice": {
            "type": "Multiple Choice",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "How many types of sentences are there based on structure?", "options": ["2", "3", "4", "5"], "correct_answer": "4", "marks": 1},
                {"question_id": 2, "question": "What is a simple sentence?", "options": ["Short sentence", "One independent clause", "Multiple clauses", "No verbs"], "correct_answer": "One independent clause", "marks": 1},
                {"question_id": 3, "question": "Which is a compound sentence?", "options": ["The cat and dog ran", "The cat ran, and the dog jumped", "When the cat ran", "The running cat"], "correct_answer": "The cat ran, and the dog jumped", "marks": 1},
                {"question_id": 4, "question": "What joins independent clauses in a compound sentence?", "options": ["Because", "Although", "Coordinating conjunction", "Subordinating clause"], "correct_answer": "Coordinating conjunction", "marks": 1},
                {"question_id": 5, "question": "What is a complex sentence?", "options": ["A long sentence", "One independent + one dependent clause", "Multiple clauses", "Complicated words"], "correct_answer": "One independent + one dependent clause", "marks": 1},
                {"question_id": 6, "question": "Which is a dependent clause marker?", "options": ["and", "but", "because", "or"], "correct_answer": "because", "marks": 1},
                {"question_id": 7, "question": "What type is: 'Although it was raining, we went outside.'?", "options": ["Simple", "Compound", "Complex", "Complex-compound"], "correct_answer": "Complex", "marks": 1},
                {"question_id": 8, "question": "A complex-compound sentence has:", "options": ["1 independent clause", "2 independent clauses", "2+ independent + 1+ dependent", "Only dependent clauses"], "correct_answer": "2+ independent + 1+ dependent", "marks": 1},
                {"question_id": 9, "question": "Which connects independent clauses?", "options": ["Subordinating conjunction", "Coordinating conjunction", "Preposition", "Article"], "correct_answer": "Coordinating conjunction", "marks": 1},
                {"question_id": 10, "question": "What is a dependent clause?", "options": ["A complete thought", "Cannot stand alone", "Has only nouns", "Needs no verb"], "correct_answer": "Cannot stand alone", "marks": 1}
            ]
        },
        "true_false": {
            "type": "True/False",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "A simple sentence has only one verb.", "correct_answer": False, "marks": 1},
                {"question_id": 2, "question": "A compound sentence joins two independent clauses.", "correct_answer": True, "marks": 1},
                {"question_id": 3, "question": "A dependent clause expresses a complete thought.", "correct_answer": False, "marks": 1},
                {"question_id": 4, "question": "Coordinating conjunctions connect equal elements.", "correct_answer": True, "marks": 1},
                {"question_id": 5, "question": "Subordinating conjunctions show relationships between clauses.", "correct_answer": True, "marks": 1},
                {"question_id": 6, "question": "A complex sentence has at least one dependent clause.", "correct_answer": True, "marks": 1},
                {"question_id": 7, "question": "All sentences must be complex.", "correct_answer": False, "marks": 1},
                {"question_id": 8, "question": "A semicolon can join independent clauses.", "correct_answer": True, "marks": 1},
                {"question_id": 9, "question": "Dependent clauses always come first in sentences.", "correct_answer": False, "marks": 1},
                {"question_id": 10, "question": "Sentence variety improves writing.", "correct_answer": True, "marks": 1}
            ]
        },
        "fill_in_blanks": {
            "type": "Fill in the Blanks",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "A _____ sentence has one independent clause.", "correct_answer": "simple", "marks": 1},
                {"question_id": 2, "question": "A _____ sentence joins two independent clauses.", "correct_answer": "compound", "marks": 1},
                {"question_id": 3, "question": "A _____ sentence has one independent and one dependent clause.", "correct_answer": "complex", "marks": 1},
                {"question_id": 4, "question": "_____ conjunctions connect independent clauses.", "correct_answer": "Coordinating", "marks": 1},
                {"question_id": 5, "question": "_____ conjunctions introduce dependent clauses.", "correct_answer": "Subordinating", "marks": 1},
                {"question_id": 6, "question": "A _____ clause cannot stand alone.", "correct_answer": "dependent", "marks": 1},
                {"question_id": 7, "question": "An _____ clause expresses a complete thought.", "correct_answer": "independent", "marks": 1},
                {"question_id": 8, "question": "A _____ joins independent clauses without a conjunction.", "correct_answer": "semicolon", "marks": 1},
                {"question_id": 9, "question": "Sentence _____ improves writing quality.", "correct_answer": "variety", "marks": 1},
                {"question_id": 10, "question": "Both _____ and subordinating conjunctions are important.", "correct_answer": "coordinating", "marks": 1}
            ]
        },
        "sentence_correction": {
            "type": "Sentence Correction",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "The cat ran and the dog jumps.", "correct_answer": "The cat ran and the dog jumped.", "marks": 1},
                {"question_id": 2, "question": "She loves reading. But she don't write.", "correct_answer": "She loves reading, but she doesn't write.", "marks": 1},
                {"question_id": 3, "question": "He studied hard because he want to pass.", "correct_answer": "He studied hard because he wanted to pass.", "marks": 1},
                {"question_id": 4, "question": "When she arrives we will begin.", "correct_answer": "When she arrives, we will begin.", "marks": 1},
                {"question_id": 5, "question": "The book is interesting and it is long.", "correct_answer": "The book is interesting and long.", "marks": 1},
                {"question_id": 6, "question": "Although it rained the game continued.", "correct_answer": "Although it rained, the game continued.", "marks": 1},
                {"question_id": 7, "question": "She plays piano and violin she sings too.", "correct_answer": "She plays piano and violin, and she sings too.", "marks": 1},
                {"question_id": 8, "question": "After he left. I went to bed.", "correct_answer": "After he left, I went to bed.", "marks": 1},
                {"question_id": 9, "question": "The team won because their coach was smart.", "correct_answer": "The team won because their coach was smart.", "marks": 1},
                {"question_id": 10, "question": "I like coffee but tea is nice.", "correct_answer": "I like coffee, but tea is nice.", "marks": 1}
            ]
        },
        "short_answer": {
            "type": "Short Answer",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "What is a simple sentence?", "correct_answer": "A sentence with one independent clause and no dependent clauses", "marks": 1},
                {"question_id": 2, "question": "Define a compound sentence.", "correct_answer": "A sentence with two or more independent clauses joined by a coordinating conjunction", "marks": 1},
                {"question_id": 3, "question": "What is a complex sentence?", "correct_answer": "A sentence with one independent clause and at least one dependent clause", "marks": 1},
                {"question_id": 4, "question": "Name three coordinating conjunctions.", "correct_answer": "and, but, or, nor, for, yet, so (any three)", "marks": 1},
                {"question_id": 5, "question": "Give five subordinating conjunctions.", "correct_answer": "because, although, if, when, while, after, before, since (any five)", "marks": 1},
                {"question_id": 6, "question": "What is an independent clause?", "correct_answer": "A clause that expresses a complete thought and can stand alone", "marks": 1},
                {"question_id": 7, "question": "What is a dependent clause?", "correct_answer": "A clause that cannot express a complete thought and cannot stand alone", "marks": 1},
                {"question_id": 8, "question": "How do coordinating conjunctions differ from subordinating?", "correct_answer": "Coordinating joins equal elements, subordinating shows hierarchy/relationship", "marks": 1},
                {"question_id": 9, "question": "What punctuation joins independent clauses without a conjunction?", "correct_answer": "A semicolon", "marks": 1},
                {"question_id": 10, "question": "Why is sentence variety important?", "correct_answer": "It makes writing more interesting and prevents monotony", "marks": 1}
            ]
        }
    }
}

remaining_quizzes.append(lesson_7)

# Lesson 8: Common Grammar Mistakes
lesson_8 = {
    "lesson_slug": "common-grammar-mistakes",
    "lesson_title": "Common Grammar Mistakes",
    "quiz_types": {
        "multiple_choice": {
            "type": "Multiple Choice",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "Which is incorrect?", "options": ["Its a beautiful day", "It's a beautiful day", "It is a beautiful day", "B and C"], "correct_answer": "Its a beautiful day", "marks": 1},
                {"question_id": 2, "question": "Choose the correct sentence:", "options": ["Their going to the store", "There going to the store", "They're going to the store", "Theyre going to the store"], "correct_answer": "They're going to the store", "marks": 1},
                {"question_id": 3, "question": "What is wrong with 'She and me went'?", "options": ["Nothing", "'She and I went' is correct", "'Me and her' is better", "'Us went' is correct"], "correct_answer": "'She and I went' is correct", "marks": 1},
                {"question_id": 4, "question": "Choose correct: 'Between you and _____'", "options": ["me", "I", "myself", "we"], "correct_answer": "me", "marks": 1},
                {"question_id": 5, "question": "What's wrong with 'Running down the street, the bus went by'?", "options": ["Nothing", "Dangling modifier", "Wrong tense", "Spelling error"], "correct_answer": "Dangling modifier", "marks": 1},
                {"question_id": 6, "question": "Which uses apostrophe correctly?", "options": ["The cats are running", "The cat's are running", "The cats' toys", "The cats's toys"], "correct_answer": "The cats' toys", "marks": 1},
                {"question_id": 7, "question": "Choose the correct comparison:", "options": ["She is more smarter", "She is more smart", "She is smarter", "She is smarterer"], "correct_answer": "She is smarter", "marks": 1},
                {"question_id": 8, "question": "What's the issue with 'However I felt, I smiled'?", "options": ["Nothing", "Needs comma after 'However'", "However should be 'how'", "Should use 'and'"], "correct_answer": "Needs comma after 'However'", "marks": 1},
                {"question_id": 9, "question": "Which is correct?", "options": ["Could of done it", "Could have done it", "Could had done it", "Could do it had"], "correct_answer": "Could have done it", "marks": 1},
                {"question_id": 10, "question": "What mistake appears in 'The team play well'?", "options": ["Spelling", "Tense", "Subject-verb disagreement", "Punctuation"], "correct_answer": "Subject-verb disagreement", "marks": 1}
            ]
        },
        "true_false": {
            "type": "True/False",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "'Its' and 'it's' are always interchangeable.", "correct_answer": False, "marks": 1},
                {"question_id": 2, "question": "'They're' means 'they are'.", "correct_answer": True, "marks": 1},
                {"question_id": 3, "question": "'Me and him' is grammatically correct.", "correct_answer": False, "marks": 1},
                {"question_id": 4, "question": "Dangling modifiers can confuse meaning.", "correct_answer": True, "marks": 1},
                {"question_id": 5, "question": "Apostrophes show plural forms.", "correct_answer": False, "marks": 1},
                {"question_id": 6, "question": "Double comparatives like 'more smarter' are incorrect.", "correct_answer": True, "marks": 1},
                {"question_id": 7, "question": "'Could of' is a common mistake for 'could have'.", "correct_answer": True, "marks": 1},
                {"question_id": 8, "question": "Run-on sentences combine independent clauses without proper punctuation.", "correct_answer": True, "marks": 1},
                {"question_id": 9, "question": "Comma splices join two sentences with a comma.", "correct_answer": True, "marks": 1},
                {"question_id": 10, "question": "Sentence fragments are always incorrect.", "correct_answer": True, "marks": 1}
            ]
        },
        "fill_in_blanks": {
            "type": "Fill in the Blanks",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "'Its' shows _____ while 'it's' means 'it is'.", "correct_answer": "possession", "marks": 1},
                {"question_id": 2, "question": "'There' refers to a _____, 'their' shows possession.", "correct_answer": "place", "marks": 1},
                {"question_id": 3, "question": "A _____ modifier confuses meaning by seeming to refer to the wrong subject.", "correct_answer": "dangling", "marks": 1},
                {"question_id": 4, "question": "Apostrophes show _____ or contractions.", "correct_answer": "possession", "marks": 1},
                {"question_id": 5, "question": "A _____ sentence combines independent clauses without proper punctuation.", "correct_answer": "run-on", "marks": 1},
                {"question_id": 6, "question": "A _____ splice uses a comma to join two independent clauses.", "correct_answer": "comma", "marks": 1},
                {"question_id": 7, "question": "A _____ fragment is an incomplete sentence.", "correct_answer": "sentence", "marks": 1},
                {"question_id": 8, "question": "Double _____ like 'more bigger' are incorrect.", "correct_answer": "comparatives", "marks": 1},
                {"question_id": 9, "question": "'Could have' is often mistakenly written as 'could _____'.", "correct_answer": "of", "marks": 1},
                {"question_id": 10, "question": "Between two people, use _____ not 'between you and I'.", "correct_answer": "me", "marks": 1}
            ]
        },
        "sentence_correction": {
            "type": "Sentence Correction",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "Its a beautiful day.", "correct_answer": "It's a beautiful day.", "marks": 1},
                {"question_id": 2, "question": "Their going to their house.", "correct_answer": "They're going to their house.", "marks": 1},
                {"question_id": 3, "question": "She and me went to the store.", "correct_answer": "She and I went to the store.", "marks": 1},
                {"question_id": 4, "question": "Running down the street, the bus went by.", "correct_answer": "As I ran down the street, the bus went by.", "marks": 1},
                {"question_id": 5, "question": "She is more smarter than him.", "correct_answer": "She is smarter than him.", "marks": 1},
                {"question_id": 6, "question": "Could of been better.", "correct_answer": "Could have been better.", "marks": 1},
                {"question_id": 7, "question": "The team play well.", "correct_answer": "The team plays well.", "marks": 1},
                {"question_id": 8, "question": "Between you and I this is a secret.", "correct_answer": "Between you and me, this is a secret.", "marks": 1},
                {"question_id": 9, "question": "She went to the store she bought milk.", "correct_answer": "She went to the store, and she bought milk.", "marks": 1},
                {"question_id": 10, "question": "Working on the project, all the ideas came to me.", "correct_answer": "While working on the project, I got all the ideas.", "marks": 1}
            ]
        },
        "short_answer": {
            "type": "Short Answer",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "What is the difference between 'its' and 'it's'?", "correct_answer": "'Its' shows possession, 'it's' means 'it is'", "marks": 1},
                {"question_id": 2, "question": "Explain the correct use of 'there', 'their', and 'they're'.", "correct_answer": "there=place, their=possession, they're=they are", "marks": 1},
                {"question_id": 3, "question": "What is a dangling modifier?", "correct_answer": "A modifier that seems to describe the wrong subject", "marks": 1},
                {"question_id": 4, "question": "Why shouldn't you say 'could of'?", "correct_answer": "Because the correct phrase is 'could have'", "marks": 1},
                {"question_id": 5, "question": "What is a run-on sentence?", "correct_answer": "Two independent clauses joined without proper punctuation", "marks": 1},
                {"question_id": 6, "question": "What is a comma splice?", "correct_answer": "Two independent clauses joined only by a comma", "marks": 1},
                {"question_id": 7, "question": "Give an example of a sentence fragment.", "correct_answer": "Running quickly through the park. / Because she was tired.", "marks": 1},
                {"question_id": 8, "question": "What is wrong with 'double comparatives'?", "correct_answer": "Using 'more' before an adjective that already ends in -er", "marks": 1},
                {"question_id": 9, "question": "Should you use 'between you and me' or 'between you and I'?", "correct_answer": "'Between you and me' because 'me' is an object pronoun", "marks": 1},
                {"question_id": 10, "question": "How do you fix a run-on sentence?", "correct_answer": "Add punctuation, use a conjunction, or split into separate sentences", "marks": 1}
            ]
        }
    }
}

remaining_quizzes.append(lesson_8)

# Lesson 9: Paragraph Writing
lesson_9 = {
    "lesson_slug": "paragraph-writing",
    "lesson_title": "Paragraph Writing",
    "quiz_types": {
        "multiple_choice": {
            "type": "Multiple Choice",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "What is the main purpose of a topic sentence?", "options": ["To be entertaining", "To introduce main idea", "To end the paragraph", "To add details"], "correct_answer": "To introduce main idea", "marks": 1},
                {"question_id": 2, "question": "Where should a topic sentence typically appear?", "options": ["At the end", "In the middle", "At the beginning", "Anywhere"], "correct_answer": "At the beginning", "marks": 1},
                {"question_id": 3, "question": "What is the function of supporting sentences?", "options": ["End the topic", "Develop and support the main idea", "Introduce new topics", "Draw conclusions"], "correct_answer": "Develop and support the main idea", "marks": 1},
                {"question_id": 4, "question": "What is a concluding sentence?", "options": ["A new topic", "A summary of the main idea", "A question", "An example"], "correct_answer": "A summary of the main idea", "marks": 1},
                {"question_id": 5, "question": "What should supporting sentences contain?", "options": ["Random facts", "Evidence and examples", "New topics", "Opinions"], "correct_answer": "Evidence and examples", "marks": 1},
                {"question_id": 6, "question": "What is coherence in writing?", "options": ["Pretty sentences", "Logical flow and connection", "Long paragraphs", "Many adjectives"], "correct_answer": "Logical flow and connection", "marks": 1},
                {"question_id": 7, "question": "What are transition words used for?", "options": ["Decoration", "Connecting ideas", "Spelling", "Grammar only"], "correct_answer": "Connecting ideas", "marks": 1},
                {"question_id": 8, "question": "Which is a transition word?", "options": ["Beautiful", "Therefore", "Quickly", "Never"], "correct_answer": "Therefore", "marks": 1},
                {"question_id": 9, "question": "What makes a paragraph unified?", "options": ["Length", "Interesting words", "All sentences support main idea", "No punctuation"], "correct_answer": "All sentences support main idea", "marks": 1},
                {"question_id": 10, "question": "What should NOT be in a paragraph?", "options": ["Topic sentence", "Supporting details", "Unrelated ideas", "Concluding sentence"], "correct_answer": "Unrelated ideas", "marks": 1}
            ]
        },
        "true_false": {
            "type": "True/False",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "Every paragraph needs a topic sentence.", "correct_answer": True, "marks": 1},
                {"question_id": 2, "question": "Topic sentences should always be at the end.", "correct_answer": False, "marks": 1},
                {"question_id": 3, "question": "Coherence means logical organization.", "correct_answer": True, "marks": 1},
                {"question_id": 4, "question": "Unity means all sentences relate to one main idea.", "correct_answer": True, "marks": 1},
                {"question_id": 5, "question": "Transition words are optional.", "correct_answer": False, "marks": 1},
                {"question_id": 6, "question": "Supporting sentences should be vague.", "correct_answer": False, "marks": 1},
                {"question_id": 7, "question": "A concluding sentence restates the main idea.", "correct_answer": True, "marks": 1},
                {"question_id": 8, "question": "Paragraphs can be any length.", "correct_answer": False, "marks": 1},
                {"question_id": 9, "question": "Examples strengthen supporting sentences.", "correct_answer": True, "marks": 1},
                {"question_id": 10, "question": "Topic sentences must be questions.", "correct_answer": False, "marks": 1}
            ]
        },
        "fill_in_blanks": {
            "type": "Fill in the Blanks",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "A _____ sentence states the main idea of the paragraph.", "correct_answer": "topic", "marks": 1},
                {"question_id": 2, "question": "_____ sentences develop and support the main idea.", "correct_answer": "Supporting", "marks": 1},
                {"question_id": 3, "question": "A _____ sentence restates or concludes the paragraph.", "correct_answer": "concluding", "marks": 1},
                {"question_id": 4, "question": "_____ refers to logical flow and connection.", "correct_answer": "Coherence", "marks": 1},
                {"question_id": 5, "question": "_____ means all sentences relate to one main idea.", "correct_answer": "Unity", "marks": 1},
                {"question_id": 6, "question": "_____ words connect ideas between sentences.", "correct_answer": "Transition", "marks": 1},
                {"question_id": 7, "question": "Supporting sentences should include _____ and examples.", "correct_answer": "evidence", "marks": 1},
                {"question_id": 8, "question": "Good paragraphs have _____, unity, and coherence.", "correct_answer": "focus", "marks": 1},
                {"question_id": 9, "question": "Transition words like 'however', 'therefore', and '_____ help flow.", "correct_answer": "moreover", "marks": 1},
                {"question_id": 10, "question": "A weak paragraph may lack a clear _____ sentence.", "correct_answer": "topic", "marks": 1}
            ]
        },
        "sentence_correction": {
            "type": "Sentence Correction",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "The paragraph have good structure.", "correct_answer": "The paragraph has good structure.", "marks": 1},
                {"question_id": 2, "question": "Supporting sentences should be vague and general.", "correct_answer": "Supporting sentences should be specific and detailed.", "marks": 1},
                {"question_id": 3, "question": "The topic sentence usually comes in the end.", "correct_answer": "The topic sentence usually comes at the beginning.", "marks": 1},
                {"question_id": 4, "question": "Transition word such as however helps connection.", "correct_answer": "Transition words such as however help connection.", "marks": 1},
                {"question_id": 5, "question": "Coherence is not important in writing.", "correct_answer": "Coherence is important in writing.", "marks": 1},
                {"question_id": 6, "question": "All sentences should relate to the topic idea.", "correct_answer": "All sentences should relate to the main idea.", "marks": 1},
                {"question_id": 7, "question": "Unity mean all ideas support the main point.", "correct_answer": "Unity means all ideas support the main point.", "marks": 1},
                {"question_id": 8, "question": "A concluding sentence should introduce a new topic.", "correct_answer": "A concluding sentence should summarize the main idea.", "marks": 1},
                {"question_id": 9, "question": "Therefore is not a transition word.", "correct_answer": "Therefore is a transition word.", "marks": 1},
                {"question_id": 10, "question": "Paragraphs can discuss any random ideas.", "correct_answer": "Paragraphs should focus on one main idea.", "marks": 1}
            ]
        },
        "short_answer": {
            "type": "Short Answer",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "What is a topic sentence?", "correct_answer": "A sentence that states the main idea of the paragraph", "marks": 1},
                {"question_id": 2, "question": "What do supporting sentences do?", "correct_answer": "They develop and support the main idea with evidence and examples", "marks": 1},
                {"question_id": 3, "question": "What is the role of a concluding sentence?", "correct_answer": "To summarize or restate the main idea", "marks": 1},
                {"question_id": 4, "question": "Define coherence.", "correct_answer": "Logical organization and clear connection between ideas", "marks": 1},
                {"question_id": 5, "question": "Define unity in a paragraph.", "correct_answer": "All sentences relate to and support one main idea", "marks": 1},
                {"question_id": 6, "question": "Give three examples of transition words.", "correct_answer": "however, therefore, moreover, furthermore, in addition (any three)", "marks": 1},
                {"question_id": 7, "question": "Why are examples important in supporting sentences?", "correct_answer": "They provide concrete evidence to support the main idea", "marks": 1},
                {"question_id": 8, "question": "What should be included in a well-developed paragraph?", "correct_answer": "Topic sentence, supporting details/examples, and concluding sentence", "marks": 1},
                {"question_id": 9, "question": "How long should a paragraph be?", "correct_answer": "Usually 5-8 sentences, depending on topic and purpose", "marks": 1},
                {"question_id": 10, "question": "What makes a paragraph weak?", "correct_answer": "Lack of clear topic sentence, poor support, or unrelated ideas", "marks": 1}
            ]
        }
    }
}

remaining_quizzes.append(lesson_9)

# Lesson 10: Practical English for Daily Use
lesson_10 = {
    "lesson_slug": "practical-english-for-daily-use",
    "lesson_title": "Practical English for Daily Use",
    "quiz_types": {
        "multiple_choice": {
            "type": "Multiple Choice",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "How do you politely ask for something?", "options": ["Give it to me", "Can you give me?", "May I have this?", "I need it"], "correct_answer": "May I have this?", "marks": 1},
                {"question_id": 2, "question": "What is the best response to 'How are you?'", "options": ["I am fine, thank you", "Nothing", "How are you?", "Very well"], "correct_answer": "I am fine, thank you", "marks": 1},
                {"question_id": 3, "question": "How do you introduce yourself?", "options": ["Who are you?", "My name is...", "You know me?", "I am..."], "correct_answer": "My name is...", "marks": 1},
                {"question_id": 4, "question": "When should you say 'thank you'?", "options": ["Never", "When receiving help", "Always", "Sometimes"], "correct_answer": "When receiving help", "marks": 1},
                {"question_id": 5, "question": "What do you say when someone says 'thank you'?", "options": ["Thank you too", "You're welcome", "That's okay", "Don't mention it"], "correct_answer": "You're welcome", "marks": 1},
                {"question_id": 6, "question": "How do you apologize?", "options": ["I apologize", "I'm sorry", "Both A and B", "Neither"], "correct_answer": "Both A and B", "marks": 1},
                {"question_id": 7, "question": "What is a polite greeting?", "options": ["Hey", "Good morning", "What's up?", "Yo"], "correct_answer": "Good morning", "marks": 1},
                {"question_id": 8, "question": "How do you ask for permission?", "options": ["Do this for me", "May I do this?", "Can I do?", "I will do"], "correct_answer": "May I do this?", "marks": 1},
                {"question_id": 9, "question": "What should you do in a conversation?", "options": ["Interrupt", "Listen carefully", "Ignore others", "Talk only"], "correct_answer": "Listen carefully", "marks": 1},
                {"question_id": 10, "question": "How do you express disagreement politely?", "options": ["You're wrong", "I respectfully disagree", "That's stupid", "No way"], "correct_answer": "I respectfully disagree", "marks": 1}
            ]
        },
        "true_false": {
            "type": "True/False",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "It's important to use 'please' and 'thank you'.", "correct_answer": True, "marks": 1},
                {"question_id": 2, "question": "Interrupting during conversation is polite.", "correct_answer": False, "marks": 1},
                {"question_id": 3, "question": "You should greet people when you meet them.", "correct_answer": True, "marks": 1},
                {"question_id": 4, "question": "Listening is more important than talking in conversation.", "correct_answer": True, "marks": 1},
                {"question_id": 5, "question": "You should apologize if you make a mistake.", "correct_answer": True, "marks": 1},
                {"question_id": 6, "question": "Being on time is not important.", "correct_answer": False, "marks": 1},
                {"question_id": 7, "question": "You can be rude if you're busy.", "correct_answer": False, "marks": 1},
                {"question_id": 8, "question": "Asking for help is a sign of weakness.", "correct_answer": False, "marks": 1},
                {"question_id": 9, "question": "You should ask permission before using someone's things.", "correct_answer": True, "marks": 1},
                {"question_id": 10, "question": "Respect and courtesy are important in daily life.", "correct_answer": True, "marks": 1}
            ]
        },
        "fill_in_blanks": {
            "type": "Fill in the Blanks",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "When you receive help, say '_____'.", "correct_answer": "thank you", "marks": 1},
                {"question_id": 2, "question": "'_____ morning' is a polite greeting.", "correct_answer": "Good", "marks": 1},
                {"question_id": 3, "question": "When someone says 'thank you', respond with '_____'.", "correct_answer": "you're welcome", "marks": 1},
                {"question_id": 4, "question": "To apologize, say 'I am _____'.", "correct_answer": "sorry", "marks": 1},
                {"question_id": 5, "question": "When asking for something, use the word '_____'.", "correct_answer": "please", "marks": 1},
                {"question_id": 6, "question": "To request permission, use '_____'.", "correct_answer": "may", "marks": 1},
                {"question_id": 7, "question": "In conversation, it's important to _____ to others.", "correct_answer": "listen", "marks": 1},
                {"question_id": 8, "question": "Being _____ is important in any conversation.", "correct_answer": "respectful", "marks": 1},
                {"question_id": 9, "question": "My name is _____, what is yours?", "correct_answer": "John/[any name]", "marks": 1},
                {"question_id": 10, "question": "To disagree politely, say 'I _____ disagree'.", "correct_answer": "respectfully", "marks": 1}
            ]
        },
        "sentence_correction": {
            "type": "Sentence Correction",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "Give me that book.", "correct_answer": "May I have that book, please?", "marks": 1},
                {"question_id": 2, "question": "I don't care what you think.", "correct_answer": "I respectfully have a different opinion.", "marks": 1},
                {"question_id": 3, "question": "You are wrong.", "correct_answer": "I respectfully disagree with you.", "marks": 1},
                {"question_id": 4, "question": "I is sorry.", "correct_answer": "I am sorry.", "marks": 1},
                {"question_id": 5, "question": "Thanks not needed.", "correct_answer": "Thank you, that's not necessary.", "marks": 1},
                {"question_id": 6, "question": "I wants to ask you something.", "correct_answer": "I want to ask you something.", "marks": 1},
                {"question_id": 7, "question": "Can I uses your pen?", "correct_answer": "May I use your pen?", "marks": 1},
                {"question_id": 8, "question": "Good morning, how is you?", "correct_answer": "Good morning, how are you?", "marks": 1},
                {"question_id": 9, "question": "You're welcome not needed.", "correct_answer": "You're welcome.", "marks": 1},
                {"question_id": 10, "question": "Listen carefully what I say.", "correct_answer": "Listen carefully to what I say.", "marks": 1}
            ]
        },
        "short_answer": {
            "type": "Short Answer",
            "total_questions": 10,
            "questions": [
                {"question_id": 1, "question": "How would you politely ask for a glass of water?", "correct_answer": "May I have a glass of water, please?", "marks": 1},
                {"question_id": 2, "question": "What is an appropriate greeting?", "correct_answer": "Good morning / Good afternoon / How are you?", "marks": 1},
                {"question_id": 3, "question": "How would you introduce yourself?", "correct_answer": "My name is [name] / I'm [name]", "marks": 1},
                {"question_id": 4, "question": "What should you do if you make a mistake?", "correct_answer": "Apologize and say sorry", "marks": 1},
                {"question_id": 5, "question": "How do you express disagreement politely?", "correct_answer": "I respectfully disagree / I have a different opinion", "marks": 1},
                {"question_id": 6, "question": "What's important in a good conversation?", "correct_answer": "Listening, being respectful, and thoughtful responses", "marks": 1},
                {"question_id": 7, "question": "When should you use 'please'?", "correct_answer": "When asking for something or making a request", "marks": 1},
                {"question_id": 8, "question": "What does 'you're welcome' mean?", "correct_answer": "A polite response to thank you", "marks": 1},
                {"question_id": 9, "question": "How would you ask permission to do something?", "correct_answer": "May I do this? / Can I do this?", "marks": 1},
                {"question_id": 10, "question": "Why is being on time important?", "correct_answer": "It shows respect for others and their time", "marks": 1}
            ]
        }
    }
}

remaining_quizzes.append(lesson_10)

# Save all remaining quizzes
with open("quizzes_remaining_lessons.json", "w") as f:
    json.dump({"quizzes": remaining_quizzes}, f, indent=2)

print(f"✓ Generated quizzes for {len(remaining_quizzes)} additional lessons")
print(f"✓ Each lesson has 50 real questions (5 types × 10 each)")
print(f"✓ Saved to quizzes_remaining_lessons.json")
print(f"\nLessons covered:")
for quiz in remaining_quizzes:
    print(f"  - {quiz['lesson_title']}")
