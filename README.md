# GPA & CGPA Calculator

A simple and interactive Java-based command-line application to calculate your Grade Point Average (GPA) for a single semester and your Cumulative Grade Point Average (CGPA) across multiple semesters.

## Features

- **Calculate GPA**: Input multiple subjects with their credits and grades to compute your semester GPA.
- **Calculate CGPA**: Input your GPAs and total credits for various semesters to find out your overall CGPA.
- **Percentage Conversion**: Automatically calculates the equivalent percentage based on your CGPA.
- **Grade Points Guide**: View the grading scale used for the calculation.

## Grading Scale

The calculator uses the following grade point mapping:

| Grade | Points |
|-------|--------|
| O     | 10     |
| A+    | 9      |
| A     | 8      |
| B+    | 7      |
| B     | 6      |
| C     | 5      |
| P     | 4      |
| F     | 0      |

## Project Structure

- `Main.java`: The entry point for the application. Handles user interactions and CLI menu.
- `Calculator.java`: Core logic for computing GPA, CGPA, and equivalent percentage.
- `Subject.java`: Model class representing a subject with its name, credit, and grade.
- `Semester.java`: Model class representing a semester containing a collection of subjects.

## Prerequisites

- Java Development Kit (JDK) 8 or higher installed on your machine.

## How to Run

1. Clone or download the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Compile the Java files:
   ```bash
   javac *.java
   ```
4. Run the application:
   ```bash
   java Main
   ```

## Usage

Once you run the program, you will be presented with a menu:

1. **Calculate GPA**: Enter the number of subjects, and for each subject, input its name, credits, and acquired grade.
2. **Calculate CGPA**: Enter the number of semesters, and for each semester, input the GPA and total credits. The app will return your overall CGPA and percentage.
3. **View Grade Points**: Displays the Grade to Point mapping.
4. **Exit**: Closes the application.
