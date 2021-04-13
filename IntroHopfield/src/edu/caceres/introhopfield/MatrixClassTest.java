package edu.caceres.introhopfield;

public class MatrixClassTest {

    public static void main(String[] args) {
        // zero matrix test.
        Matrix zero = new Matrix(5, 5);
        System.out.println(zero);

        // boolean matrix test.
        boolean[][] booleans = new boolean[5][5];
        for(int r=0; r<booleans.length; r++) {
            for(int c=0; c<booleans[0].length; c++) {
                booleans[r][c] = (r+c)%2==0;
            }
        }
        System.out.println(new Matrix(booleans));

        // column and row matrix tests.
        double[] doubles = {1, 2, 3, 4, 5};
        System.out.println(Matrix.createRowMatrix(doubles));
        System.out.println(Matrix.createColumnMatrix(doubles));
    }

}
