import java.util.ArrayList;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\n=====================");
            System.out.println(" GPA & CGPA Calculator ");
            System.out.println("=======================");
            System.out.println("1. Calculate GPA");
            System.out.println("2. Calculate CGPA");
            System.out.println("3. View Grade Points");
            System.out.println("4. Exit");
            System.out.print("Enter your choice: ");

            int choice = readInt(sc);

            switch (choice) {
                case 1:
                    calculateGPA(sc);
                    break;
                case 2:
                    calculateCGPA(sc);
                    break;
                case 3:
                    showGradePoints();
                    break;
                case 4:
                    System.out.println("Exiting... Thank you!");
                    sc.close();
                    return;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }
    }

    private static void calculateGPA(Scanner sc) {
        ArrayList<Subject> subjects = new ArrayList<>();

        System.out.print("Enter number of subjects: ");
        int n = readInt(sc);

        for (int i = 1; i <= n; i++) {
            System.out.println("\nSubject " + i);

            System.out.print("Enter subject name: ");
            String name = sc.nextLine();

            System.out.print("Enter credits: ");
            int credits = readInt(sc);

            System.out.print("Enter grade (O, A+, A, B+, B, C, P, F): ");
            String grade = sc.nextLine();

            subjects.add(new Subject(name, credits, grade));
        }

        try {
            double gpa = Calculator.calculateGPA(subjects);
            System.out.printf("\nYour GPA is: %.2f%n", gpa);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void calculateCGPA(Scanner sc) {
        System.out.print("Enter number of semesters: ");
        int n = readInt(sc);

        double[] gpas = new double[n];
        int[] credits = new int[n];

        for (int i = 0; i < n; i++) {
            System.out.println("\nSemester " + (i + 1));

            System.out.print("Enter GPA: ");
            gpas[i] = readDouble(sc);

            System.out.print("Enter total credits: ");
            credits[i] = readInt(sc);
        }

        double cgpa = Calculator.calculateCGPA(gpas, credits);
        double percentage = Calculator.percentageFromCGPA(cgpa);

        System.out.printf("\nYour CGPA is: %.2f%n", cgpa);
        System.out.printf("Equivalent Percentage: %.2f%%%n", percentage);
    }

    private static void showGradePoints() {
        System.out.println("\nGrade Point Mapping:");
        System.out.println("O  = 10");
        System.out.println("A+ = 9");
        System.out.println("A  = 8");
        System.out.println("B+ = 7");
        System.out.println("B  = 6");
        System.out.println("C  = 5");
        System.out.println("P  = 4");
        System.out.println("F  = 0");
    }

    private static int readInt(Scanner sc) {
        while (true) {
            try {
                String input = sc.nextLine();
                return Integer.parseInt(input.trim());
            } catch (NumberFormatException e) {
                System.out.print("Enter a valid integer: ");
            }
        }
    }

    private static double readDouble(Scanner sc) {
        while (true) {
            try {
                String input = sc.nextLine();
                return Double.parseDouble(input.trim());
            } catch (NumberFormatException e) {
                System.out.print("Enter a valid number: ");
            }
        }
    }
}