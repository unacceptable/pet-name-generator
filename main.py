from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import uvicorn
import os

VERSION = os.environ.get('VERSION', 'v0.1.0')

app = FastAPI(
    title='Pet Name Generator API',
    description='A delightful API for generating creative pet names',
    version=VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Mount static files
app.mount('/static', StaticFiles(directory='static'), name='static')

# Pet name data
DOG_NAMES = [
    'Buddy', 'Max', 'Charlie', 'Cooper', 'Rocky', 'Bear', 'Duke', 'Zeus',
    'Tucker', 'Jack', 'Oliver', 'Leo', 'Milo', 'Teddy', 'Finn', 'Oscar',
    'Luna', 'Bella', 'Daisy', 'Lucy', 'Molly', 'Sadie', 'Sophie', 'Chloe',
    'Lola', 'Zoe', 'Penny', 'Nala', 'Stella', 'Ruby', 'Rosie', 'Lily'
]

CAT_NAMES = [
    'Whiskers', 'Shadow', 'Mittens', 'Tiger', 'Smokey', 'Oreo', 'Felix',
    'Simba', 'Garfield', 'Chester', 'Jasper', 'Oscar', 'Leo', 'Max',
    'Luna', 'Chloe', 'Bella', 'Lucy', 'Lily', 'Sophie', 'Princess',
    'Cleo', 'Nala', 'Zoe', 'Gracie', 'Penny', 'Molly', 'Daisy'
]

BIRD_NAMES = [
    'Tweety', 'Sunny', 'Blue', 'Charlie', 'Kiwi', 'Mango', 'Rio',
    'Skye', 'Pepper', 'Sunny', 'Rainbow', 'Echo', 'Phoenix', 'Storm',
    'Angel', 'Pearl', 'Ruby', 'Jewel', 'Crystal', 'Jade', 'Coral'
]

FISH_NAMES = [
    'Nemo', 'Dory', 'Bubbles', 'Fin', 'Splash', 'Goldie', 'Neptune',
    'Coral', 'Pearl', 'Aqua', 'Marina', 'Blue', 'Sunny', 'Flash',
    'Shimmer', 'Glimmer', 'Sparkle', 'Wave', 'Current', 'Tide'
]

RABBIT_NAMES = [
    'Bunny', 'Thumper', 'Cottontail', 'Snowball', 'Pepper', 'Cocoa',
    'Hazel', 'Clover', 'Sage', 'Basil', 'Honey', 'Sugar', 'Cinnamon',
    'Nutmeg', 'Ginger', 'Caramel', 'Mocha', 'Vanilla', 'Butterscotch'
]

# Pet facts data
PET_FACTS = {
    'dog': [
        "Dogs have three eyelids: upper, lower, and a third lid called the nictitating membrane!",
        "A dog's sense of smell is 10,000 to 100,000 times stronger than humans!",
        "Dogs can learn over 150 words and can count up to four or five!",
        "The basenji dog is known as the 'barkless dog' because it doesn't bark like other dogs!",
        "Dogs sweat through their paw pads and cool down by panting!"
    ],
    'cat': [
        "Cats have 32 muscles in each ear, allowing them to rotate their ears 180 degrees!",
        "A group of cats is called a 'clowder' and a group of kittens is called a 'kindle'!",
        "Cats spend 70% of their lives sleeping - that's 13 to 16 hours a day!",
        "A cat's purr vibrates at a frequency that promotes bone healing!",
        "Cats can make over 100 different sounds, while dogs can only make about 10!"
    ],
    'bird': [
        "Birds are the only living descendants of dinosaurs!",
        "The Arctic tern has the longest migration of any bird, flying from Arctic to Antarctic annually!",
        "Hummingbirds can fly backwards and are the only birds that can hover in place!",
        "Parrots can live over 100 years, with some macaws living up to 120 years!",
        "Birds don't have teeth - they use their gizzards to grind up food!",
    ],
    'fish': [
        "Fish have been on Earth for over 500 million years!",
        "Some fish, like the lungfish, can survive out of water for months!",
        "Goldfish can see in four colors: red, green, blue, and ultraviolet!",
        "The oldest known goldfish lived to 43 years old!",
        "Fish don't have eyelids, so they sleep with their eyes open!",
    ],
    'rabbit': [
        "Rabbits can see behind them without turning their heads due to their eye placement!",
        "A rabbit's teeth never stop growing throughout their entire life!",
        "Rabbits can jump nearly 3 feet high and 10 feet long!",
        "Baby rabbits are called 'kits' and are born blind and hairless!",
        "Rabbits can live 8-12 years with proper care and can be litter trained like cats!",
    ]
}

PET_NAMES_DB = {
    'dog': DOG_NAMES,
    'cat': CAT_NAMES,
    'bird': BIRD_NAMES,
    'fish': FISH_NAMES,
    'rabbit': RABBIT_NAMES
}

class PetNameResponse(BaseModel):
    pet_type: str
    names: List[str]
    count: int


class HealthResponse(BaseModel):
    status: str
    message: str


class PetFactResponse(BaseModel):
    pet_type: str
    fact: str


class PetFactsResponse(BaseModel):
    pet_type: str
    facts: List[str]
    total_facts: int


@app.get('/', include_in_schema=False)
async def serve_frontend():
    '''
    Serve the frontend application.
    '''
    return FileResponse('static/index.html')


@app.get('/health', response_model=HealthResponse)
async def health_check():
    '''
    Health check endpoint.
    '''
    return HealthResponse(
        status='healthy',
        message='Pet Name Generator API is running smoothly! 🐾'
    )


@app.get('/pets', response_model=dict)
async def get_available_pets():
    '''
    Get list of available pet types.
    '''
    return {
        'available_pets': list(PET_NAMES_DB.keys()),
        'total_types': len(PET_NAMES_DB)
    }


@app.get('/pets/{pet_type}/names', response_model=PetNameResponse)
async def get_pet_names(
    pet_type: str,
    count: int = 1,
    random_selection: bool = True
):
    '''
    Generate pet names for a specific pet type.

    - **pet_type**: Type of pet (dog, cat, bird, fish, rabbit)
    - **count**: Number of names to return (1-10)
    - **random_selection**: Whether to randomly select names or return in order
    '''
    pet_type = pet_type.lower()

    if pet_type not in PET_NAMES_DB:
        raise HTTPException(
            status_code=404,
            detail=f"Pet type '{pet_type}' not found. Available types: {list(PET_NAMES_DB.keys())}"
        )

    if count < 1 or count > 10:
        raise HTTPException(
            status_code=400,
            detail='Count must be between 1 and 10'
        )

    available_names = PET_NAMES_DB[pet_type]

    if random_selection:
        selected_names = random.sample(
            available_names,
            min(count, len(available_names))
        )
    else:
        selected_names = available_names[:count]

    return PetNameResponse(
        pet_type=pet_type,
        names=selected_names,
        count=len(selected_names)
    )


@app.get('/pets/{pet_type}/random', response_model=dict)
async def get_random_pet_name(pet_type: str):
    '''
    Get a single random name for a specific pet type.
    '''
    pet_type = pet_type.lower()

    if pet_type not in PET_NAMES_DB:
        raise HTTPException(
            status_code=404,
            detail=f"Pet type '{pet_type}' not found. Available types: {list(PET_NAMES_DB.keys())}"
        )

    random_name = random.choice(PET_NAMES_DB[pet_type])

    return {
        'pet_type': pet_type,
        'name': random_name,
        'message': f'Perfect name for your {pet_type}! 🐾'
    }


@app.get('/pets/{pet_type}/facts', response_model=PetFactsResponse)
async def get_pet_facts(pet_type: str):
    '''
    Get all facts for a specific pet type.
    '''
    pet_type = pet_type.lower()

    if pet_type not in PET_FACTS:
        raise HTTPException(
            status_code=404,
            detail=f"Pet type '{pet_type}' not found. Available types: {list(PET_FACTS.keys())}"
        )

    facts = PET_FACTS[pet_type]

    return PetFactsResponse(
        pet_type=pet_type,
        facts=facts,
        total_facts=len(facts)
    )


@app.get('/pets/{pet_type}/facts/random', response_model=PetFactResponse)
async def get_random_pet_fact(pet_type: str):
    '''
    Get a random fact for a specific pet type.
    '''
    pet_type = pet_type.lower()

    if pet_type not in PET_FACTS:
        raise HTTPException(
            status_code=404,
            detail=f"Pet type '{pet_type}' not found. Available types: {list(PET_FACTS.keys())}"
        )

    random_fact = random.choice(PET_FACTS[pet_type])

    return PetFactResponse(
        pet_type=pet_type,
        fact=random_fact
    )


@app.get('/facts', response_model=dict)
async def get_all_facts():
    '''
    Get all facts for all pet types.
    '''
    all_facts = []

    for pet_type, facts in PET_FACTS.items():
        all_facts.extend([{'pet_type': pet_type, 'fact': fact} for fact in facts])

    return {
        'facts': all_facts,
        'total_facts': len(all_facts),
        'pet_types': list(PET_FACTS.keys())
    }


@app.get('/facts/random', response_model=PetFactResponse)
async def get_random_fact():
    '''
    Get a random fact from any pet type.
    '''
    # Get all facts from all pet types
    all_facts = []

    for pet_type, facts in PET_FACTS.items():
        for fact in facts:
            all_facts.append({'pet_type': pet_type, 'fact': fact})

    random_fact_data = random.choice(all_facts)

    return PetFactResponse(
        pet_type=random_fact_data['pet_type'],
        fact=random_fact_data['fact']
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
