# Mew's Tavern API

---

## Table of Contents

- [Project Links](#project-links)
- [UX](#ux)
- [Models & Database](#models--database)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Testing](#testing)
  - [Manual Testing](#manual-testing)
  - [Bugs](#bugs)
  - [Unsolved Bugs](#unsolved-bugs)
- [Technologies Used](#technologies-used)
  - [Main Languages](#main-languages)
  - [Frameworks, Libraries & Programs](#frameworks-libraries--programs)
- [Deployment](#deployment)
- [Credits](#credits)
  - [Code](#code)

---

# Project Links

This project was created with a two repositories, the separate being the frontend.
Links to the frontend part of the project can be found in the links below:
[Frontend Repo]()
[Live Link]()

---

# UX

---

# Models & Database

The initial design for the database models has been modified quite a bit throughout the project, it's similar to the initial plan but some of the models was "extended".
This is the final outcome:

![LucidChart](/readme_assets/p5relationshipdiagram.png)

Additional models in the 'pokemons' app consists of Ability, Move, Type, Nature and HeldItem. They all have consist of one 'name' CharField.
The Ability, Move and Type models are connected to the Pokemon model with ManyToMany, while Nature and HeldItem are used for the PokemonBuild model and are ForeignKeys.

- All data in the Pokemon model was extracted from an external API, PokéAPI.
- Files were created to extract the data I wanted into a JSON file, then I created BaseCommands which was used to populate my database with the JSON files that was created.
- As I had read that the PokéAPI could be quite slow due to it's popularity, and also because I wanted to limit the Pokémon data I decided that it was better to have the data stored in my database instead of getting the data directly from its external source.

---

# Features

---

# Testing

## Manual Testing

Manual testing was done throughout the developement of the project to make sure the API was working as intended. This was done by creating several superusers and testing the CRUD functionality at existing endpoints.

## Automated Testing

---

## Technologies Used

### Main Languages

- Python

### Frameworks, Libraries & Programs

- Django - Main python framework used to to develop the application
- [GitHub](https://github.com/) - To save and store files for the website.
- Git - For version control.
- [Heroku](https://www.heroku.com/) - For deploying the project
- [ElephantSQL]() - Was used as the database for this project
- [Cloudinary](https://cloudinary.com/) - For hosting media files

---

## Deployment

This project was deployed with Heroku, following the steps of Code Institute's [deployment cheatsheet](https://docs.google.com/document/d/1v8mOyB5l7aSL5loy3MVIX4z4SsLYKe-ZEGGpT_Z5DRM/edit#).

### Forking and cloning

If you'd want to experiment and work on this code you can fork or clone this project.
This will allow you do whatever you want without altering the original.

#### Steps to forking:

- In the repository, navigate to the "Fork" button which is located in the top-right of the page, next to "Star".
- Simply click on this button and a copy of this repository will be added to yours.

#### Cloning:

- Navigate to the top right of this repository and find the button labelled "Code", and click to display a dropdown menu.
- Here you can either:
  - Choose the option "Download as ZIP" which will download all files and save a copy locally.
  - Choose the option "Open with Github Desktop" and work from there.

---

## Credits

