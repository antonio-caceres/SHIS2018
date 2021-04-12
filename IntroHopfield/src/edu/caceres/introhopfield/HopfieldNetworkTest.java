package edu.caceres.introhopfield;

public class HopfieldNetworkTest {

    public static void main(String[] args) {
        boolean[] pattern = {true, false, true, false, true, true};

        HopfieldNetwork neuralNet = new HopfieldNetwork(pattern.length);
        System.out.println(neuralNet.getWeightMatrix());

        neuralNet.train(pattern);
        System.out.println(neuralNet.getWeightMatrix());

        System.out.println("RESULTS");
        boolean[] processedPattern = neuralNet.present(pattern);
        for (boolean b : processedPattern)
            System.out.print(BiPolarUtil.boolToBipolar(b) + " ");
        System.out.println();

        boolean[] patternTwo = {false, true, false, true, false, true};
        boolean[] processedPatternTwo = neuralNet.present(patternTwo);
        for (boolean b : processedPatternTwo)
            System.out.print(BiPolarUtil.boolToBipolar(b) + " ");
        System.out.println();

        boolean[] patternThree = {true, false, true, true, true, false};
        boolean[] processedPatternThree = neuralNet.present(patternThree);
        for (boolean b : processedPatternThree)
            System.out.print(BiPolarUtil.boolToBipolar(b) + " ");
        System.out.println();

        boolean[] patternFour = {false, false, true, false, true, false};
        boolean[] processedPatternFour = neuralNet.present(patternFour);
        for (boolean b : processedPatternFour)
            System.out.print(BiPolarUtil.boolToBipolar(b) + " ");
        System.out.println();

        boolean[] patternFive = {false, true, false, false, true, true}; // WHY DOES THIS GO TO INVERSE PATTERN ONE AAAAAAAAAAAAAAAAAAAA
        boolean[] processedPatternFive = neuralNet.present(patternFive);
        for (boolean b : processedPatternFive)
            System.out.print(BiPolarUtil.boolToBipolar(b) + " ");
        System.out.println();
    }
}
