from fastapi import FastAPI, Depends, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId

from database import get_database
from schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse
)

app = FastAPI(title="Organization API")

COLLECTION = "organizations"


@app.get("/")
def health_check():
    return {"status": "ok"}



#POST
@app.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_organization(
    organization: OrganizationCreate,
    db=Depends(get_database)
):
    result = await db[COLLECTION].insert_one(organization.dict())
    org = await db[COLLECTION].find_one({"_id": result.inserted_id})

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "industry": org["industry"],
        "size": org["size"]
    }

#GET ALL ORGANIZATION
@app.get(
    "/organizations",
    response_model=list[OrganizationResponse]
)
async def get_all_organizations(db=Depends(get_database)):
    organizations = []

    cursor = db[COLLECTION].find()
    async for org in cursor:
        organizations.append({
            "id": str(org["_id"]),
            "name": org["name"],
            "industry": org["industry"],
            "size": org["size"]
        })

    return organizations

#GET - Organization by id
@app.get(
    "/organizations/{organization_id}",
    response_model=OrganizationResponse
)
async def get_organization_by_id(
    organization_id: str,
    db=Depends(get_database)
):
    try:
        object_id = ObjectId(organization_id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid organization ID"
        )

    org = await db[COLLECTION].find_one({"_id": object_id})

    if not org:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "industry": org["industry"],
        "size": org["size"]
    }



#PUT - Upddate the organization
@app.put(
    "/organizations/{organization_id}",
    response_model=OrganizationResponse
)
async def update_organization(
    organization_id: str,
    organization: OrganizationUpdate,
    db=Depends(get_database)
):
    try:
        object_id = ObjectId(organization_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid organization ID")

    update_data = {k: v for k, v in organization.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    result = await db[COLLECTION].update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    org = await db[COLLECTION].find_one({"_id": object_id})

    return {
        "id": str(org["_id"]),
        "name": org["name"],
        "industry": org["industry"],
        "size": org["size"]
    }


#DELETE - remove the organization
@app.delete(
    "/organizations/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_organization(
    organization_id: str,
    db=Depends(get_database)
):
    try:
        object_id = ObjectId(organization_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid organization ID")

    result = await db[COLLECTION].delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )