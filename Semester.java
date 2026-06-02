import java.util.ArrayList;
public class Semester {
    private ArrayList<Subject> subjects;

    public Semester(){
        subjects = new ArrayList<>();
    }

    public void addSubject(Subject s){
        subjects.add(s);
    }

    public ArrayList<Subject> getSubjects() {
        return subjects;
    }
}
