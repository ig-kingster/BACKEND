from fastapi import FastAPI, HTTPException, File, UploadFile,Form
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os
import aiofiles
from fastapi.staticfiles import StaticFiles

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

DATABASE_NAME = "db_jetsetgo"


UPLOAD_DIR = "uploads"  # Directory to save uploaded files



# Utility function to save the file
async def save_file(file: UploadFile, upload_dir: str) -> str:
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    return file_path





# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    mongo_client = AsyncIOMotorClient(MONGO_URI)
    db = mongo_client[DATABASE_NAME]
    app.state.db = db  # Attach the database to app.state
    print("Connected to MongoDB")
    yield
    # Shutdown logic
    await mongo_client.close()
    print("MongoDB connection closed")

app = FastAPI(lifespan=lifespan)


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Admin(BaseModel):
    admin_name : str
    admin_photo : str
    admin_email : str
    admin_password  : str

   
@app.post("/admin/")
async def create_admin(admin:Admin):
    admin_data = admin.model_dump()
    result = await app.state.db["tbl_admin"].insert_one(admin_data)
    return{"id": str(result.inserted_id),"message": "admin added sucessfully"}


class State(BaseModel):
    state_name : str
   
@app.post("/state")
async def create_state(state:State):
    state_data = state.model_dump()
    result = await app.state.db["state"].insert_one(state_data)
    return{"id": str(result.inserted_id),"message": "state added sucessfully"}


@app.get("/state")
async def read_state():
    cursor = app.state.db["state"].find()
    stateData = await cursor.to_list(length=None)  # Convert cursor to list
    for state in stateData:
        state["_id"] = str(state["_id"])
    if not stateData:
        raise HTTPException(status_code=404, detail="Item not found")
    return stateData


class District(BaseModel):
   district_name : str
   state_id : str

@app.post("/district/")
async def create_district(district:District):
    district_data =district.model_dump()
    result = await app.state.db["district"].insert_one(district_data)
    return{"id": str(result.inserted_id),"message": "district added sucessfully"}

class Place(BaseModel):
    place_name : str
    district_id: str

@app.post("/place/")
async def create_place(place:Place):
    place_data = place.model_dump()
    result = await app.state.db["tbl_place"].insert_one(place_data)
    return{"id": str(result.inserted_id),"message": "place added sucessfully"}


class Hotel(BaseModel):
    hotel_name  : str
    hotel_email : str
    hotel_address  : str
    hotel_phone_no : int
    place_id  : str
    hotel_proof : str
    hotel_photo : str
    hotel_status : str
    hotel_room_count : int
    hotel_password : str


   
@app.post("/hotel/")
async def create_hotel(hotel:Hotel):
    hotel_data = hotel.model_dump()
    result = await app.state.db["tbl_hotel"].insert_one(hotel_data)
    return{"id": str(result.inserted_id),"message": "hotel added sucessfully"}


class User(BaseModel):
    user_name : str
    user_email : str
    user_phone_number : int
    place_id : str
    user_idproof : str
    user_photo : str
    user_password : str



 
@app.post('/user')
async def create_user(user:User):
    user_data = user.model_dump()
    result = await app.state.db["tbl_user"].insert_one(user_data)
    return{"id": str(result.inserted_id),"message": "user added sucessfully"}



class Guide(BaseModel):
    guide_name : str
    guide_email : str
    guide_phone_number : int
    guide_proof : str
    guide_photo : str
    guide_status : str
    guide_password : str
    hotel_id : str



 
@app.post("/guide/")
async def create_guide(guide:Guide):
    guide_data = guide.model_dump()
    result = await app.state.db["tbl_guide"].insert_one(guide_data)
    return{"id": str(result.inserted_id),"message": "guide added sucessfully"}


class Packagehead(BaseModel):
    packagehead_days : str
    packagehead_price : int
    packagehead_details : str
    packagehead_status : str
    packagehead_count : str
    packagehead_room_count : str



@app.post("/packagehead/")
async def create_packagehead(packagehead:Packagehead):
    packagehead_data = packagehead.model_dump()
    result = await app.state.db["tbl_packagehead"].insert_one(packagehead_data)
    return{"id": str(result.inserted_id),"message": "packagehead added sucessfully"}



class Packagebody(BaseModel):
    packagebody_details : str
    place_id : str
    packagehead_id : str


@app.post("/packagebody/")
async def create_packagebody(packagebody:Packagebody):
    packagebody_data = packagebody.model_dump()
    result = await app.state.db["tbl_packagebody"].insert_one(packagebody_data)
    return{"id": str(result.inserted_id),"message": "packagebody added sucessfully"}


class Gallery(BaseModel):
    packagebody_id : str
    gallery_file : str
    gallery_description : str



@app.post("/gallery/")
async def create_gallery(gallery:Gallery):
    gallery_data = gallery.model_dump()
    result = await app.state.db["tbl_gallery"].insert_one(gallery_data)
    return{"id": str(result.inserted_id),"message": "gallery added sucessfully"}


class Booking(BaseModel):
    booking_date : str
    booking_for_date : str
    booking_status : str
    booking_to_date : str
    packagehead_id : str
    user_id : str
    booking_status : str
    guide_id : str
    booking_amount : int


@app.post("/booking/")
async def create_booking(booking:Booking):
    booking_data = booking.model_dump()
    result = await app.state.db["tbl_booking"].insert_one(booking_data)
    return{"id": str(result.inserted_id),"message": "booking added sucessfully"}


class Userinfo(BaseModel):
    userinfo_name : str
    userinfo_number : int
    booking_id : str



@app.post("/userinfo/")
async def create_userinfo(userinfo:Userinfo):
    userinfo_data = userinfo.model_dump()
    result = await app.state.db["tbl_userinfo"].insert_one(userinfo_data)
    return{"id": str(result.inserted_id),"message": "userinfo added sucessfully"}


class Rating(BaseModel):
    user_id : str
    guide_id : str
    hotel_id : str
    rating_contact : int
    rating_count : int


@app.post("/rating/")
async def create_rating(rating:Rating):
    rating_data = rating.model_dump()
    result = await app.state.db["tbl_rating"].insert_one(rating_data)
    return{"id": str(result.inserted_id),"message": "rating added sucessfully"}



class Complaint(BaseModel):
    complaint_title : str
    complaint_contact : str
    complaint_reply : str
    complaint_status : str
    user_id : str


@app.post("/complaint/")
async def create_complaint(complaint:Complaint):
    complaint_data = complaint.model_dump()
    result = await app.state.db["tbl_complaint"].insert_one(complaint_data)
    return{"id": str(result.inserted_id),"message": "complaint added sucessfully"}







@app.post("/fileUp/")
async def create_user(
    photo: UploadFile = File(...),
):
    try:
        # Save the file
        saved_filename = await save_file(photo, UPLOAD_DIR)
        file_url = f"http://127.0.0.1:8000/{saved_filename}"

        # Insert data into MongoDB
        user_data = { "photo": file_url}
        result = await app.state.db["photoUpload"].insert_one(user_data)

        return {
            "id": str(result.inserted_id),
            "message": "User created successfully",
            "file_path": file_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


