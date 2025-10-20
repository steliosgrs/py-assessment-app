Ο χρήστης θα μπορεί να κάνει μόνο login. Ο λογαρασμός θα είναι προ-δημιουργημένος, αφού ο κάθε χρήστης θα έχει ήδη εγγραφεί μέσω μιας ξεχωριστής διαδικασίας εκτός της εφαρμογής Streamlit.

# Roadmap for Integrating MongoDB with Repository Pattern

## Overview

To enhance the flexibility and scalability of our project, we are implementing the Repository Pattern to abstract our data access layer. This will allow us to seamlessly switch between Firestore and MongoDB as our database backends based on environment configurations.

## Goals

- Implement the Repository Pattern to decouple data access logic from business logic.
- Create repository interfaces for
  - User data
  - Exercises
- Implement concrete repository classes for both Firestore and MongoDB.
- Update the application to use the repository layer for all data operations.

## Implementation Steps

1. **Define Repository Interfaces**
   - Create abstract base classes for UserRepository and ExerciseRepository in `shared/database/repositories/`.
2. **Implement Firestore Repositories**
   - Implement FirestoreUserRepository and FirestoreExerciseRepository in `shared/database/firestore/`.
3. **Implement MongoDB Repositories**
   - Implement MongoUserRepository and MongoExerciseRepository in `shared/database/mongodb/`.
4. **Database Connection Setup**
   - Set up connection handling for both Firestore and MongoDB in their respective directories.
5. **Environment Configuration**
   - Use environment variables to determine which database to use (e.g., `DATABASE=firestore` or `DATABASE=mongodb`).
6. **Update Application Logic**
   - Refactor the application code in `streamlit_app/` and `shared/course_loader.py` to utilize the repository interfaces for all data operations.
7. **Testing**
   - Thoroughly test both database implementations to ensure data integrity and application functionality.

## Pages to Update

- Login Page (`streamlit_app/pages/login.py`): Update to use UserRepository for authentication.
- Exercises Page (`streamlit_app/pages/exercises.py`): Update to fetch exercises via ExerciseRepository.
- Modules Page (`streamlit_app/pages/modules.py`): Update to fetch modules via ModuleRepository.
- About us Page (`streamlit_app/pages/about_us.py`): No changes needed.

## Components

- Login functionality only; user registration is handled externally.
- Account

# Roadmap Exercise Testing Module

## Motivation

To ensure the reliability and correctness of our exercise management functionalities, we will develop a dedicated testing module. This module will facilitate unit and integration testing for the exercise-related components of our application.

## Goals

- Create a testing module specifically for exercise functionalities.
- Implement unit tests for individual functions and methods.
- Implement integration tests to verify the interaction between different components.

## Implementation Steps

1. **Set Up Testing Framework**
   - Choose a testing framework (e.g., pytest) and set up the necessary configurations.
2. **Create Test Cases**
   - Develop unit tests for core functions in `shared/exercise_runner.py`.
   - Develop integration tests to cover end-to-end scenarios involving exercise data retrieval and manipulation.
3. **Mocking and Fixtures**
   - Use mocking to simulate database interactions for isolated unit tests.
   - Create fixtures for common test data setups.
4. **Continuous Integration**
   - Integrate the testing module into the CI/CD pipeline to ensure tests are run on every commit.
5. **Documentation**
   - Document the testing procedures and how to run the tests for future reference.

## Testing Focus Areas

- Exercise data retrieval and storage.
- User progress tracking.
- Error handling and edge cases.
- Performance of exercise loading and execution. management is handled externally; users can only log in.
- Use of environment variables to switch between Firestore and MongoDB.

## Pages to Update

- Exercise Runner Module (`shared/exercise_runner.py`): Implement test cases for exercise functionalities.
- Test Suite (`tests/test_exercise_runner.py`): New file to contain all test cases for the exercise runner module.

## Components

- Unit tests for individual functions in the exercise runner.
- Integration tests for end-to-end exercise workflows.
- Mocking of database interactions for isolated testing.
- Documentation for running and maintaining tests.

# Roadmap final assessment module

## Motivation

When all exercises have been completed, a final assessment module will be implemented to evaluate the user's overall understanding of the course material. This module will provide a comprehensive test covering all topics and skills learned throughout the course.

The final assessment will be assigned to each student upon completion of all exercises, ensuring that they have mastered the content before concluding the course. Given a dataset, students will be required to perform data analysis, apply relevant techniques, and present their findings in a structured format.

## Possible Datasets

- Titanic Survival Dataset
- Iris Flower Dataset
- Wine Quality Dataset
- Customer Churn Dataset
- MNIST Handwritten Digits Dataset

## Goals

- Perform Data Cleaning and Preprocessing
- Conduct Exploratory Data Analysis (EDA)
- Upload your findings in a Jupyter Notebook format
- Deploy your Marimo Notebook

## Deliverables

When a student completes the final assessment, they will be required to fill out a google form providing the following information:

- Full Name
- Email Address
- Choose one of the provided datasets
- Link to github repository containing the Jupyter Notebook with their analysis and findings.
- Any additional comments or reflections on the assessment.
- Feedback on the course and suggestions for improvement.

# Roadmap on creating a module that test the final assessment submissions

## Motivation

To ensure the quality and correctness of the final assessment submissions, we will develop a dedicated testing module. This module will facilitate the evaluation of the Jupyter Notebooks submitted by students, checking for key components such as data cleaning, analysis, and visualization.

Also, the final assessment will be automatically checked for plagiarism to maintain academic integrity. A pipeline will be set up to compare the submitted notebooks against each other and against a database of known sources.
Additionally, a judge LLM will be integrated to provide feedback on the quality of the analysis, clarity of explanations, and overall presentation of the findings.

## Goals

- Create a testing module specifically for final assessment submissions.
- Implement plagiarism detection for submitted notebooks.
- Integrate a judge LLM for qualitative feedback.
