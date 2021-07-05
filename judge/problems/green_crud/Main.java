import java.util.*;
import java.io.*;

class GreenCrudAnswer {
    /**
	* The minimum acceptable initialSize of calPopulation.
	*/
    public static final int initialSize_min = 1;
    /**
	* The maximum acceptable initialSize of calPopulation.
	*/
    public static final int initialSize_max = 10000;
    /**
	* The minimum acceptable days of calPopulation 
	*/
    public static final int days_min = 1;
    /**
	* The maximum acceptable days of calPopulation.
	*/
    public static final int days_max = 100;

    /**
	* An integer, which determines the size of the fibonacci_ with days_max. 
	*/
    private static int fibonacciSize_ = days_max / 5 + 1;

    /**
	* An integer array which stores fibonacciSize_ Fibonacci numbers.
	*/
    private static int[] fibonacci_ = new int[fibonacciSize_];

    /**
	* A boolean, which indicates if fibonacci_ has been initialized.
	*/
    private static boolean fibonacciInitialed_ = false;

    /**
	* @param initialSize The size of the green crud starts at.
	* @param days The green crud population after days days.
	* @return An integer, which is the size of the green crud population after days days, starting at an initial size of initialSize.
	*/
    public static int calPopulation(int initialSize, int days) {
        if (fibonacciInitialed_ == false) {
            fibonacci_[0] = 1;
            fibonacci_[1] = 1;

            for (int i = 2; i != fibonacciSize_; ++i) {
                fibonacci_[i] = fibonacci_[i - 1] + fibonacci_[i - 2];
            }

            fibonacciInitialed_ = true;
        }

        return initialSize * fibonacci_[days / 5];
    }
}

public class Main {
    public static void main(String[] args) {
        ResultGenerator rg =
            new ResultGenerator(args[0], List.of("GreenCrud.java"));

        Random random = new Random();

        GreenCrud gc = new GreenCrud();
        GreenCrudAnswer gc_ans = new GreenCrudAnswer();

        for (int kkk = 0; kkk != 100; ++kkk) {
            int initialSize = random.nextInt(50);
            int days = random.nextInt(100);

            try {
                String output =
                    Integer.valueOf(gc.calPopulation(initialSize, days))
                        .toString();
                String answer =
                    Integer.valueOf(gc_ans.calPopulation(initialSize, days))
                        .toString();

                if (!output.equals(answer)) {
                    rg.OutputWA(output, answer, "GreenCrud.calPopulation",
                                Integer.toString(initialSize),
                                Integer.toString(days));
                    return;
                }
            } catch (Exception e) {
                rg.OutputRE(e);
                return;
            }
        }

        rg.OutputAC();
    }
}