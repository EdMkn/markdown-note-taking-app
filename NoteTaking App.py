import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import markdown
import sqlite3
import uvicorn

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            html TEXT
        )
    """)
    conn.commit()
    conn.close()



# Model for saving notes
class Note(BaseModel):
    title: str
    content: str

# Upload and save markdown file
@app.post("/upload")
def upload_markdown(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    html_content = markdown.markdown(content)
    
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, html) VALUES (?, ?, ?)", 
                   (file.filename, content, html_content))
    conn.commit()
    conn.close()
    
    return {"message": "File uploaded successfully", "title": file.filename}

@app.post("/save")
def save_note(note: Note):
    html_content = markdown.markdown(note.content)
    
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, html) VALUES (?, ?, ?)", 
                   (note.title, note.content, html_content))
    conn.commit()
    conn.close()
    
    return {"message": "Note saved successfully", "title": note.title}

# List all notes
@app.get("/notes")
def get_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return {"notes": [{"id": n[0], "title": n[1]} for n in notes]}

# Get a specific note to check the grammar
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, html FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"title": note[0], "content": note[1], "html": note[2]}

# def delete_note(self, note_number):

def main():
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    while True:
        print("\nNote Taking Application")
    #    print("1. Add Note")
        print("2. View Notes")
        print("3. Check a Note's grammar")
    #    print("3. Delete Note")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

    #    if choice == '1':
    #        note = input("Enter your note: ")
    #        save_note(note)
        if choice == '2':
            all_notes = get_notes()
            print("Your Notes")
            for note in all_notes['notes']:
                print(f"{note['id']}. {note['title']}")
        elif choice == '3':
            num_note = int(input("insert the id of the note"))
            note = get_note(num_note)
            print(f"{num_note}. {note['title']}\n {note['html']}")

        elif choice == '4':
            print("Exiting the Note Taking Application")
            break 

if __name__ == "__main__":
    main()