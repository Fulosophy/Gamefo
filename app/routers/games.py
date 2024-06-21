from typing import List
from fastapi import APIRouter,HTTPException,Path
from app.db_connection import connect_db, fetch_as_dict
from app.models.games_model import Game


router = APIRouter()

# GET request to get games "LIKE" user query
@router.get("/games/{game_name}", tags=["Games"], response_model=List[Game])
async def get_game_many_by_query(game_title: str):
    search_query = f"%{game_title}%"  
    # Connect to the database
    if len(game_title) < 3 :
        raise HTTPException(status_code=400, detail="Query must be at least 3 characters long!")
    try: 
        conn = await connect_db()
        
    # If connection fails, return an error message
    except:
        raise Exception("Connection to database failed!")

    # Try to get the games that have a name similar to the query
    
    try:
        sql_query = "SELECT * FROM api.game_info WHERE game_title ILIKE $1 order by game_title ASC"
        params = (search_query,)
        result = await fetch_as_dict(conn, sql_query, search_query)
        
        
        # If no games are found, return an error message
        if not result:
            raise HTTPException(status_code=404, detail="No Games Found!")
        return result
    
    # If an error occurs, return the error message
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
      
        await conn.close()
    
@router.get("/games", tags=["Games"], response_model=List[Game])
async def get_all_games():
  
    # Connect to the database
    try: 
        conn = await connect_db()
        
    # If connection fails, return an error message
    except:
        raise HTTPException(status_code=500, detail="Connection to database failed!")
    # Try to get the games that have a name similar to the query
    try:
     
        sql_query = "SELECT * FROM api.game_info order by game_title ASC"
        result = await fetch_as_dict(conn, sql_query)
         
        # If no games are found, return an error message
        if not result:
            raise HTTPException(status_code=404, detail="No Games Found!")
        print(result)
        return result
    
    # If an error occurs, return the error message
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Error has occured: {str(e)}")
    finally:
        await conn.close()
    

