import java.util.ArrayList;

public class Calculator{
    public static int getGradePoint(String grade){
        switch (grade.toUpperCase()) {
            case "O": return 10;
            case "A+": return 9;
            case "A": return 8;
            case "B+": return 7;
            case "B": return 6;
            case "C": return 5;
            case "P": return 4;
            case "F": return 0;
            default: return -1;
        }
    }

    public static double calculateGPA(ArrayList<Subject> subjects) {
        int totalCredits = 0;
        int totalPoints = 0;

        for (Subject s : subjects) {
            int gp = getGradePoint(s.getGrade());
            if (gp == -1) {
                throw new IllegalArgumentException("Invalid grade: " + s.getGrade());
            }
            totalCredits += s.getCredit();
            totalPoints += s.getCredit() * gp;
        }

        if (totalCredits == 0) return 0.0;
        return (double) totalPoints / totalCredits;
    }

    public static double calculateCGPA(double[] gpas, int[] credits) {
        int totalCredits = 0;
        double weightedSum = 0.0;

        for (int i = 0; i < gpas.length; i++) {
            weightedSum += gpas[i] * credits[i];
            totalCredits += credits[i];
        }

        if (totalCredits == 0) return 0.0;
        return weightedSum / totalCredits;
    }

    public static double percentageFromCGPA(double cgpa) {
        return cgpa * 10;
    }
}