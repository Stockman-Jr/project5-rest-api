# Mew's Tavern API

Mew's Tavern is a social media site created with the purpose of being a Pokémon community for fans of the franchise.

User can create posts and share various game related content, which they can interact with by liking or commmenting. Users can also browse the PokéDex, where they can save pokémons they've caught to keep track of their collection.

This is an API built with Django Rest Framework and serves as the backend part of the project.
Live link can be found [here](https://pokeproject-api.herokuapp.com/).

---

## Table of Contents

- [Project Links](#project-links)
- [Models & Database](#models--database)
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

This project was created with two repositories, the separate being the frontend.
Links to the frontend parts of the project can be found in the links below:

[Frontend Repo](https://github.com/Stockman-Jr/mews-tavern)
[Live Link](https://mews-tavern.herokuapp.com/)

---

# Models & Database

The initial design for the database models has been modified quite a bit throughout the project, it's similar to the initial plan but some of the models was "extended".
This is the final outcome:

![LucidChart](/readme_assets/p5relationshipdiagram.png)


**Pokemons Models**

Additional models in the 'pokemons' app consists of Ability, Move, Type, Nature and HeldItem. They all have consist of one 'name' CharField.
The Ability, Move and Type models are connected to the Pokemon model with ManyToMany, while Nature and HeldItem are used for the PokemonBuild model and are ForeignKeys.

- All data in the Pokemon model was extracted from an external API, PokéAPI.
- Files were created to extract the data I wanted into a JSON file, then I created BaseCommands which was used to populate my database with the JSON files that was created.
- As I had read that the PokéAPI could be quite slow due to it's popularity, and also because I wanted to limit the Pokémon data I decided that it was better to have the data stored in my database instead of getting the data directly from its external source.

**Posts Models**

There are three models in the posts app: BasePost, Post and PokemonBuild.
The BasePost model was created as a parent model to Post and PokemonBuild.
I used and InheritanceManager for the BasePost model using a library called django-model-utils.

The Post model is used for creating posts that contains game related content, for example sharing screenshots or fan art.

The PokemonBuild model is for creating posts where users can select from the pokémons they own  to create a build from the selected pokémon.


---

# Testing

## Manual Testing

Manual testing was done throughout the developement of the project to make sure the API was working as intended. This was done by creating several superusers and testing the CRUD functionality at existing endpoints.

## Trainer Profiles

### /profiles & <int:pk>

| **Test Case**                                                 | **User Status**   | **CRUD Operation** | **Result** |
| ------------------------------------------------------------- | ----------------- | ------------------ | ---------- |
| All users can retrieve and read data from user profiles.      | Any               | Read               | Pass       |
| Users that are the owner of the profile can update it.        | Profile owner     | Update             | Pass       |
| Users that are not the owner of the profile cannot update it. | Not profile owner | Update             | Pass       |

(Creation of profile is done automatically upon user instance creation and users cannot delete their profile)

## Posts

### /posts/

| **Test Case**                                        | **User Status** | **CRUD Operation** | **Result** |
| ---------------------------------------------------- | --------------- | ------------------ | ---------- |
| All users can retrieve and read data from all posts. | Any             | Read               | Pass       |

### /posts/post & /<int:pk>

| **Test Case**                                              | **User Status** | **CRUD Operation** | **Result** |
| ---------------------------------------------------------- | --------------- | ------------------ | ---------- |
| Logged in users can create posts.                          | Logged in       | Create             | Pass       |
| Logged out users cannot create posts.                      | Logged out      | Create             | Pass       |
| All users can retrieve and read data from a single post.   | Any             | Read               | Pass       |
| Users can access their owned posts and update them.        | Post owner      | Update             | Pass       |
| Users cannot access posts they do not own and update them. | Not post owner  | Update             | Pass       |
| Users can access their owned posts and delete them.        | Post owner      | Delete             | Pass       |
| Users cannot access posts they do not own and delete them. | Not post owner  | Delete             | Pass       |

### /posts/pokebuild/ & /<int:pk>

| **Test Case**                                                                 | **User Status** | **CRUD Operation** | **Result** |
| ----------------------------------------------------------------------------- | --------------- | ------------------ | ---------- |
| Logged in users can create and share Pokémon builds.                          | Logged in       | Create             | Pass       |
| Logged out users cannot create and share Pokémon builds.                      | Logged out      | Create             | Pass       |
| Users that are the owner of the build can update their Pokémon builds.        | Build Owner     | Update             | Pass       |
| Users that are not the owner of the build cannot update their Pokémon builds. | Not build Owner | Update             | Pass       |
| Users that are the owner of the build can delete their Pokémon builds.        | Build Owner     | Delete             | Pass       |
| Users that are not the owner of the build cannot delete their Pokémon builds. | Not build Owner | Delete             | Pass       |

## Pokemons

### api/pokemons/ & api/caught/

| **Test Case**                                                     | **User Status** | **CRUD Operation** | **Result** |
| ----------------------------------------------------------------- | --------------- | ------------------ | ---------- |
| All users can retrieve and read pokémon data.                     | Any             | Read               | Pass       |
| Logged in users can save(create) pokémons they've caught.         | Logged in       | Create             | Pass       |
| Logged out users cannot save(create) caught pokémons.             | Logged out      | Create             | Pass       |
| Only users that are the owner can delete pokémons they've caught. | Pokémon Owner   | Delete             | Pass       |

## Likes

### /likes & /<int:pk>

| **Test Case**                                              | **User Status** | **CRUD Operation** | **Result** |
| ---------------------------------------------------------- | --------------- | ------------------ | ---------- |
| All users can retrieve and read data of likes.             | Any             | Read               | Pass       |
| Logged in users can like a post.                           | Logged in       | Create             | Pass       |
| Logged out users cannot like a post.                       | Logged out      | Create             | Pass       |
| Users that are the owner of the like can delete it.        | Like Owner      | Delete             | Pass       |
| Users that are not the owner of the like cannot delete it. | Not like Owner  | Delete             | Pass       |

## Comments

### /comments & /<int:pk>

| **Test Case**                                                 | **User Status**   | **CRUD Operation** | **Result** |
| ------------------------------------------------------------- | ----------------- | ------------------ | ---------- |
| All users can retrieve and read comments data.                | Any               | Read               | Pass       |
| Logged in users can create comments.                          | Logged in         | Create             | Pass       |
| Logged out users cannot create comments.                      | Logged out        | Create             | Pass       |
| Users that are the owner of the comment can update it.        | Comment Owner     | Update             | Pass       |
| Users that are not the owner of the comment cannot update it. | Not Comment Owner | Update             | Pass       |
| Users that are the owner of the comment can delete it.        | Comment Owner     | Delete             | Pass       |
| Users that are not the owner of the comment cannot delete it. | Not Comment Owner | Delete             | Pass       |

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

This project was deployed using heroku, steps to deployment are as follows:
  * Sign up to heroku if you haven't, then check for a button labelled "New" at the top right of the dashboard.
    * Click that button to display a dropdown menu and select "Create New App".
    * This will take you to a new page, where you can enter your region and choose a name for your new app, which must be unique. Then click "Create App"
  
  * On the next page, navigate to the "Settings" tab on the menu, and find the section called "Config Vars"
  * Click on the button labelled "Config Vars" and add necessary values for these keys:
      * CLOUDINARY_URL, DATABASE_URL, ALLOWED_HOST, CLIENT_ORIGIN, CLIENT_ORIGIN_DEV and SECRET_KEY

  * Scroll back to the top menu and click the "Deploy" tab.
    * Here you'll have some options for deployment, I used github for this.
    * Once you've clicked on the Github button you will be able to search for your Github repository and connect to it.
    * Once connected, it's time to deploy. You can choose to deploy automatically or manually, I chose automatic deploys for this project.

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

### Code

- [PokéAPI](https://pokeapi.co/) - Used to get the Pokémon data.
- [Stackoverflow](https://stackoverflow.com/) - Stackoverflow was used in abundance as usual when looking for solutions and fixes.
- [Code Institute](https://github.com/Code-Institute-Solutions/drf-api/tree/ed54af9450e64d71bc4ecf16af0c35d00829a106) - The moments walkthrough project was used as a base reference for this project.
- **Github Repositories**
  - Code from these repositories was used as an inspiration to create the pokemons app.
    - [Project Pokemon](https://github.com/jpozzo5/project_pokemon-) - Created by jpozzo5@github. I specifically looked at this projects pokemon models and command files so that I could populate my database.
    - [Pokemon Capstone Backend](https://github.com/r-o-e-574/pokemon-capstone-backend/tree/62a8ac26896a4c66cf972b44e10c4a072dc39729) - Created by r-o-e-574@github.
    - [Dexapp API](https://github.com/ninjaguydan/dexapp_API) - Created by ninjaguydan@github.


