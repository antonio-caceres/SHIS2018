package edu.caceres.introhopfield;

public class HopfieldNetworkTest {

    public static void main(String args[]) {
        boolean[] pattern = {true, false, true, false, true, true};

        HopfieldNetwork neuralNet = new HopfieldNetwork(pattern.length);
        System.out.println(neuralNet.getWeightMatrix());

        neuralNet.train(pattern);
        System.out.println(neuralNet.getWeightMatrix());

        System.out.println("RESULTS");
        boolean[] processedPattern = neuralNet.present(pattern);
        for(int i=0; i<processedPattern.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPattern[i]) + " ");
        System.out.println();

        boolean[] patternTwo = {false, true, false, true, false, true};
        boolean[] processedPatternTwo = neuralNet.present(patternTwo);
        for(int i=0; i<processedPatternTwo.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternTwo[i]) + " ");
        System.out.println();

        boolean[] patternThree = {true, false, true, true, true, false};
        boolean[] processedPatternThree = neuralNet.present(patternThree);
        for(int i=0; i<processedPatternThree.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternThree[i]) + " ");
        System.out.println();

        boolean[] patternFour = {false, false, true, false, true, false};
        boolean[] processedPatternFour = neuralNet.present(patternFour);
        for(int i=0; i<processedPatternFour.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternFour[i]) + " ");
        System.out.println();

        boolean[] patternFive = {false, true, false, false, true, true}; // WHY DOES THIS GO TO INVERSE PATTERN ONE AAAAAAAAAAAAAAAAAAAA
        boolean[] processedPatternFive = neuralNet.present(patternFive);
        for(int i=0; i<processedPatternFive.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternFive[i]) + " ");
        System.out.println();
    }
}
