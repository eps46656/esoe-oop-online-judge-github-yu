import java.util.*;
import java.io.*;

public class ResultGenerator {
    String token;
    List<String> filenames;

    ResultGenerator(String token) {
        this.token = token;
        this.filenames = new ArrayList<String>();
    }

    ResultGenerator(String token, List<String> filenames) {
        this.token = token;
        this.filenames = filenames;
    }

    public void OutputAC() { this.Output_("AC"); }

    public void OutputWA() { this.Output_("WA"); }

    public void OutputWA(String output, String answer, String function_name,
                         String... function_args) {
        StringBuilder sb = new StringBuilder("WA");

        sb.append("mismatch: ").append(function_name).append('(');

        if (function_args.length != 0) {
            sb.append(function_args[0]);

            for (int i = 1; i != function_args.length; ++i) {
                sb.append(", ").append(function_args[i]);
            }
        }

        this.Output_(sb.append(")\n\toutput: ")
                         .append(output)
                         .append("\n\texpected: ")
                         .append(answer)
                         .toString());
    }

    public void OutputRE() { this.Output_("RE"); }

    public void OutputRE(Exception e) {
        StringWriter sw = new StringWriter();
        sw.write("RE");

        StackTraceElement stack_trace_eles[] = e.getStackTrace();

        int i = 0;

        while (i != stack_trace_eles.length &&
               this.filenames.contains(stack_trace_eles[i].getFileName())) {
            ++i;
        }

        StackTraceElement new_stack_trace_eles[] = new StackTraceElement[i];

        for (int j = 0; j != i; ++j) {
            new_stack_trace_eles[j] = stack_trace_eles[j];
        }

        e.setStackTrace(new_stack_trace_eles);
        e.printStackTrace(new PrintWriter(sw));
        this.Output_(sw.toString());
    }

    private void Output_(String message) {
        System.out.print(message);
        System.out.print(String.format("%016x", message.length()));
        System.out.print(this.token);
    }
}