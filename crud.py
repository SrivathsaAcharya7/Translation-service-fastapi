from sqlalchemy.orm import Session
import models
import json

def create_translation_task(db:Session,text:str,languages:list):
    task=models.TranslationTask(text=text,languages=languages)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_translation_task(db:Session,task_id:int):
    return db.query(models.TranslationTask).filter(models.TranslationTask.id==task_id).first()

def update_translation_task(db:Session,task_id:int,translations:dict):
    task=db.query(models.TranslationTask).filter(models.TranslationTask.id==task_id).first()
    if task:
        print(f"Task translations before update: {translations}")
        task.translation = translations  # Make sure this is correctly serialized
        task.status = "Completed"
        db.commit()  # Commit the changes
        db.refresh(task)
        print(f"Updated task in database: {task.translation}")
        return task