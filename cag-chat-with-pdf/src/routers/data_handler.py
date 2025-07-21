from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import uuid as uuid_pkg
import os

# import the shared data store
from src.data_store import data_store


# pdf processing utility
from src.utils.pdf_processor import extract_text_from_pdf


# LLM client utility
from src.utils.llm_client import get_llm_response

router = APIRouter()

# Define temporary directory for uploads
UPLOAD_DIR = "/temp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only pdf files are accepted")
    

    uuid_str = str(uuid)
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} already exist. use PUT/api/v1/update/ {uuid_str} to append data.",
        )
    
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str} _ {file.filename}")
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

            extracted_text = extract_text_from_pdf(file_path)

            if extracted_text is None:
                raise HTTPException(
                    status_code=500, detail="Failed to extract text from PDF."
                )
            
            data_store[uuid_str] = extracted_text
            return {
                "message" : "File uploaded and text extracted successfully"
            }
        

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"An error occured during file processing: {str(e)}",
        )
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.put("/update/{uuid}")
def update_pdf_data(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid File type. only PDF file are accepted."
        )

    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail= f"UUID {uuid_str} not found.Use POST /api/v1/upload/{uuid_str} to create it first.",
        )


    file_path = os.path.join(UPLOAD_DIR,  f"{uuid_str}_update_{file.filename}")
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        new_text = extract_text_from_pdf(file_path)

        if new_text is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to extract text from PDF"
            )

        data_store[uuid_str] += "/n/n" + new_text 
        return {"message" : "Data appended successfully", "uuid" : uuid_str}


    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"An error occured during file processing: {str(e)}",
        )

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/query/{uuid}")
def query_data(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):


    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail= f"UUID {uuid_str} not found"
        )

    stored_text = data_store[uuid_str]

    llm_response = get_llm_response(context=stored_text, query=query)

    return {"uuid" : uuid_str, "query": query, "llm_response": llm_response}


@router.delete("/data/{uuid}", status_code=200)
def delete_data(uuid: uuid_pkg.UUID):
    
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404, detail= f"UUID {uuid_str} not found"
        )
    
    del data_store[uuid_str]
    return {"message" :  f" Data for UUID {uuid_str} deleted successfully"}


@router.get("/list_uuids")
def list_all_uuids():

    return {"uuids" : list(data_store.keys())}

