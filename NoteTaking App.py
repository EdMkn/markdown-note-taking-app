import os

class NoteTakingApp:
    def __init__(self, filename='notes.txt'):
        self.filename = filename
        self.load_notes()
        
    def load_notes(self):
        """ Load notes from the file """
        if os.path.exists(self.filename):
            with open(self.filename,'r') as file:
                self.notes = file.readlines()
        else:
            self.notes = []

    def save_notes(self):
        """Save notes to the file"""
        with open(self.filename,'w') as file:
            file.writelines(self.notes)

    def add_note(self, note):
        """Add a new note"""
        self.notes.append(note +'\n')
        self.save_notes()
        print("Note added!")

    def view_notes(self):
        """View all notes"""
        if not self.notes:
            print('No notes found')
        else:
            print("Your Notes")
            for index, note in enumerate(self.notes, start = 1):
                print(f"{index}. {note.strip()}")
    
    def delete_note(self, note_number):
        """Delete a note by its number"""
        if 0< note_number <=len(self.notes):
            removed_note = self.notes.pop(note_number - 1)
            self.save_notes()
            print(f'Note "{removed_note.strip()}" deleted.')
        else:
            print("Invalid note number.")

def main():
    app=NoteTakingApp()
    while True:
        print("\nNote Taking Application")
        print("1. Add Note")
        print("2. View Notes")
        print("3. Delete Note")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            note = input("Enter your note: ")
            app.add_note(note)
        elif choice == '2':
            app.view_notes()
        elif choice == '3':
            app.view_notes()
            try:
                note_number = int(input("Enter the note number you want to delete: "))
                app.delete_note(note_number)
            except ValueError:
                print("Please enter a valid number")
        elif choice == '4':
            print("Exiting the Note Taking Application")
            break

if __name__ == "__main__":
    main()