from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FlashCard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    first_column = Column(String)
    second_column = Column(String)
    box_number = Column(Integer)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def check_str_empty(text):
    if not text or text.isspace():
        return True
    else:
        return False


def add_flashcard():
    question = str(input("\nQuestion:\n"))

    while check_str_empty(question):
        question = str(input("\nQuestion:\n"))

    answer = str(input("\nAnswer:\n"))
    while check_str_empty(answer):
        answer = str(input("\nAnswer:\n"))

    values = FlashCard(first_column=question, second_column=answer, box_number=0)
    session.add(values)
    session.commit()


def edit_menu(obj):
    option = str(input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n'))
    option = option.lower()
    while check_str_empty(option) or option not in ("d", "e"):
        print(f"{option} is not an option\n")
        option = str(input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n'))
        option = option.lower()

    if option == "d":
        session.delete(obj)
        session.commit()
    else:
        print(f"current question: {obj.first_column}")
        new_question = str(input("please write a new question:\n"))
        while check_str_empty(new_question):
            new_question = str(input("please write a new question:\n"))

        print(f"current answer: {obj.second_column}")
        new_answer = str(input("please write a new answer:\n"))

        while check_str_empty(new_answer):
            new_answer = str(input("please write a new answer:\n"))

        obj.first_column = new_question
        obj.second_column = new_answer
        session.commit()

def learning_menu(obj):
    option = str(input('\npress "y" if your answer is correct:\npress "n" if your answer is wrong:\n'))
    while check_str_empty(option) or option not in ("y", "n"):
        option = str(input("\npress 'y' if your answer is correct:\npress 'n' if your answer is wrong:\n"))
    if option == 'y':
        obj.box_number += 1
        session.commit()
    elif option == 'n':
        obj.box_number = 0
        session.commit()
    if obj.box_number >= 3:
        session.delete(obj)
        session.commit()



def show_questions(num_session):
    #flashcards = session.query(FlashCard).all()
    flashcards = tuple(session.query(FlashCard).filter(FlashCard.box_number <= num_session))
    if flashcards:
        for fc in flashcards:
            question = fc.first_column
            answer = fc.second_column
            print(f"\nQuestion: {question}")
            option = str(input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n'))
            option = option.lower()

            while check_str_empty(option) or option not in ("y", "n", "u"):
                print(f"{option} is not an option\n")
                option = str(input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n'))

            if option == "y":
                print(f"\nAnswer: {answer}")
                learning_menu(fc)
            elif option == "u":
                edit_menu(fc)
                continue
            else:
                learning_menu(fc)
                continue
    else:
        print("\nThere is no flashcard to practice!")

class MemoryApplications:
    def flashcard_menu(self):
        print("""\n1. Add a new flashcard\n2. Exit
        """)
        selection = input()
        try:
            selection = int(selection)
            if selection == 1:
                add_flashcard()
                self.flashcard_menu()
            if selection == 2:
                self.welcome_screen(self.num_session)
            else:
                print(f"\n{selection} is not an option\n")
                self.flashcard_menu()
        except ValueError:
            print(f"\n{selection} is not an option\n")
            self.flashcard_menu()

    def welcome_screen(self, num_session):
        print("""\n1. Add flashcards\n2. Practice flashcards\n3. Exit""")
        selection = input()
        try:
            selection = int(selection)
            if selection == 1:
                self.flashcard_menu()
            elif selection == 2:
                show_questions(self.num_session)
                self.num_session += 1
                self.welcome_screen(self.num_session)
            elif selection == 3:
                print("\nBye!")
                exit()
            else:
                print(f"\n{selection} is not an option\n")
                self.welcome_screen(self.num_session)
        except ValueError:
            print(f"\n{selection} is not an option\n")
            self.welcome_screen(self.num_session)
    num_session = 1


def main():
    MemoryApplications().welcome_screen(MemoryApplications.num_session)


if __name__ == "__main__":
    main()