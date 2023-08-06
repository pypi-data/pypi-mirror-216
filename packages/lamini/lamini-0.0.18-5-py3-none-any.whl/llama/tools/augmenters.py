from tqdm import tqdm
from llama import Type, Context, LLMEngine
from random import sample


def get_attributes(value):
    return [
        attribute
        for attribute, _ in value.__fields__.items()
    ]


# class NovelQuestion(Type):
#     question: str = Context("a novel question, with a radically different subject")


# TODO: figure out how to work with more arbitrary Types
class AugmenterOutput(Type):
    new: str = Context("a novel one, with a different subject")


def augment_question_answer_pairs(
        seed_data,
        n=10,
        question_model_name="lamini/open",
        answer_model_name="lamini/instruct",
        doc_data=None,
        verbose=False,
    ):
    """Augment a seed data with new generated pairs of questions and answers."""
    # Enforce paired data, error with good message if not
    if not isinstance(seed_data[0], list) or not len(seed_data[0]) == 2:
        raise ValueError("Seed data for question-answer pairs must be a list of lists, where each inner list is a question-answer pair (length 2 list).")
    augmenter = QuestionAnswerAugmenter(
        seed_data,
        question_model_name=question_model_name,
        answer_model_name=answer_model_name,
        doc_data=doc_data,
    )
    return augmenter.run(n, verbose=verbose)

def augment(
        seed_data,
        n=10,
        model_name=None,
        doc_data=None,
        verbose=False,
    ):
    """Augments a dataset with more of the same Type (e.g. Question)"""
    if isinstance(seed_data[0], list):
        print("Warning: augment_questions() called with paired data, but only questions will be augmented.")
    augmenter = Augmenter(
        seed_data,
        model_name=model_name,
        doc_data=doc_data,
    )
    return augmenter.run(n, verbose=verbose)

def augment_with_answers(
        questions,
        output_type=None,
        model_name=None,
        doc_data=None,
        verbose=False,
    ):
    augmenter = AnswerAugmenter(
        questions,
        output_type=output_type,
        model_name=model_name,
        doc_data=doc_data,
    )
    return augmenter.run(verbose=verbose)


class Augmenter:
    def __init__(self, seed_data, model_name="lamini/open", doc_data=None):
        self.seed_data = seed_data

        self.model_name = model_name
        self.llm = LLMEngine(id="lamini-augmenter", model_name=self.model_name)
        self.input_type = type(self.__get_inputs()[0])
        data = self.__make_pairs()
        if doc_data:
            data += doc_data
        self.llm.add_data(data)
        
        self.augmentations = []
    
    def __get_first_attribute(self):
        return get_attributes(self.input_type)[0]

    def __get_inputs(self):
        if type(self.seed_data[0]) is list:
            return [datum[0] for datum in self.seed_data]
        return self.seed_data

    def __make_pairs(self):
        seed_inputs = self.__get_inputs()
        pairs = []
        for seed_input in seed_inputs:
            other = sample(seed_inputs, 1)[0]

            # pairs.append([seed, NovelQuestion(question=other.question)])
            pairs.append([seed_input, AugmenterOutput(new=other[self.__get_first_attribute()])])

        return pairs

    def run(self, n, verbose=False):
        for i in tqdm(range(n)):
            # Go through all the seed data once, then repeat if n is larger than the seed data
            datum = self.seed_data[i % len(self.seed_data)]
            
            # If there are multiple elements, then assume the first one is the type user wants to augment, e.g. Question
            datum_to_llm = datum[0] if isinstance(datum, list) else datum

            # out = self.llm(datum_to_llm, type(datum_to_llm))
            # out = self.llm(datum_to_llm, NovelQuestion, temperature=0.7, max_tokens=32)
            out = self.llm(datum_to_llm, AugmenterOutput, temperature=0.7)
            out = type(datum_to_llm)(**{self.__get_first_attribute(): out.new})
            self.augmentations.append(out)
            
            if verbose:
                print('Augmenter Input', datum_to_llm)
                print('Augmenter Output', out)

        return self.augmentations


class AnswerAugmenter:
    def __init__(self, questions, output_type=None, model_name="lamini/instruct", seed_data=None, doc_data=None):
        assert isinstance(questions[0], list) or output_type is not None, "Must provide output_type if questions are not paired with an Answer type."
        self.questions = questions # e.g. questions

        # If there are multiple elements, then assume the last one is Answer type
        self.output_type = output_type if output_type is not None else type(questions[0][-1]) # e.g. Answer type

        self.model_name = model_name
        self.llm = LLMEngine(id="lamini-answer-augmenter", model_name=self.model_name)
        data = []
        if seed_data:
            data += seed_data
        if doc_data:
            data += doc_data
        self.llm.add_data(data)
        
        self.augmentations = []

    def run(self, verbose=False):
        # Iterate through all questions and generate answers
        for datum in tqdm(self.questions):
            # If there are multiple elements, then assume the first one is the input, e.g. Question
            datum_to_llm = datum[0] if isinstance(datum, list) else datum
            answer = self.llm(datum_to_llm, self.output_type)
            # answer = self.llm(datum_to_llm, self.output_type, temperature=0.0, max_tokens=128)
            self.augmentations.append(answer)
            if verbose:
                print('AnswerAugmenter Input', datum_to_llm)
                print('AnswerAugmenter Output', answer)
        return self.augmentations


class QuestionAnswerAugmenter: # TODO: eventually inherit from generic DataAugmenter class
    """Build a dataset from seed data of question-answer pairs and augment them with new generated data."""

    def __init__(self, seed_data, question_model_name="lamini/open", answer_model_name="lamini/instruct", doc_data=None):
        assert isinstance(seed_data[0], list), "Seed data must be a list of lists, where each inner list is a question-answer pair (length 2 list)."

        self.seed_data = seed_data
        
        self.question_type = type(seed_data[0][0])
        self.answer_type = type(seed_data[0][1])

        self.question_model_name = question_model_name
        self.answer_model_name = answer_model_name

        # self.question_llm = LLMEngine(id="lamini-q-augmenter", model_name=self.question_model_name)
        # self.answer_llm = LLMEngine(id="lamini-a-augmenter", model_name=self.answer_model_name)
        self.doc_data = doc_data
        
        self.augmentations = [] # Question-Answer pairs
    
    def run(self, n, verbose=False):
        augmented_questions = Augmenter(self.seed_data, model_name=self.question_model_name, doc_data=self.doc_data).run(n, verbose=verbose)
        augmented_answers = AnswerAugmenter(augmented_questions, output_type=self.answer_type, model_name=self.answer_model_name, seed_data=self.seed_data, doc_data=self.doc_data).run(verbose=verbose)
        self.augmentations = list(zip(augmented_questions, augmented_answers))
        return self.augmentations
