package edu.caceres.introhopfield;

public class BiPolarUtil {

    public static double boolToBipolar(final boolean b) {
        if (b) {
            return 1;
        } else {
            return -1;
        }
    }

    public static double[] boolToBipolar(final boolean b[]) {
        final double[] result = new double[b.length];

        for (int i = 0; i < b.length; i++) {
            result[i] = BiPolarUtil.boolToBipolar(b[i]);
        }

        return result;
    }

    public static double[][] boolToBipolar(final boolean b[][]) {
        final double[][] result = new double[b.length][b[0].length];

        for (int r = 0; r < b.length; r++) {
            for (int c = 0; c < b[0].length; c++) {
                result[r][c] = BiPolarUtil.boolToBipolar(b[r][c]);
            }
        }

        return result;
    }

    public static boolean bipolarToBool(final double d) {
        if (d > 0) {
            return true;
        } else {
            return false;
        }
    }

    public static boolean[] bipolarToBool(final double d[]) {
        final boolean[] result = new boolean[d.length];

        for (int i = 0; i < d.length; i++) {
            result[i] = bipolarToBool(d[i]);
        }

        return result;
    }

    public static boolean[][] bipolarToBool(final double d[][]) {
        final boolean[][] result = new boolean[d.length][d[0].length];

        for (int r = 0; r < d.length; r++) {
            for (int c = 0; c < d[0].length; c++) {
                result[r][c] = bipolarToBool(d[r][c]);
            }
        }

        return result;
    }

    /**
     *
     * @param num
     * @return 0 if num is negative; 1 if num is positive
     */
    public static double binaryStepFunction(final double num) {
        if (num > 0)
            return 1;
        else
            return 0;
    }

    public static double bipolarToBinary(final double num) {
        return (num + 1) / 2.0;
    }

    public static double binaryToBipolar(final double num) {
        return num * 2.0 - 1;
    }
}
