package edu.caceres.introhopfield;

public class HopfieldNetworkTest {

    public static void main(String args[]) {
        boolean[] pattern = {true, false, true, false};

        HopfieldNetwork neuralNet = new HopfieldNetwork(pattern.length);
        System.out.println(neuralNet.getWeightMatrix());

        neuralNet.train(pattern);
        System.out.println(neuralNet.getWeightMatrix());
        boolean[] processedPattern = neuralNet.present(pattern);
        for(int i=0; i<processedPattern.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPattern[i]) + " ");
        System.out.println();

        boolean[] patternTwo = {false, true, false, true};
        boolean[] processedPatternTwo = neuralNet.present(patternTwo);
        for(int i=0; i<processedPatternTwo.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternTwo[i]) + " ");
        System.out.println();

        boolean[] patternThree = {true, true, true, true};
        boolean[] processedPatternThree = neuralNet.present(patternThree);
        for(int i=0; i<processedPatternThree.length; i++)
            System.out.print(BiPolarUtil.boolToBipolar(processedPatternThree[i]) + " ");
        System.out.println();
    }
}
