package edu.caceres.introhopfield;

public class MatrixMathClassTest {

    public static void main(String[] args) {
        double[][] sourceA = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        double[][] sourceB = {{4, 3, 2}, {6, 5, 4}, {3, 2, 1}};

        Matrix matrixA = new Matrix(sourceA);
        Matrix matrixB = new Matrix(sourceB);

        System.out.println(matrixA);
        System.out.println(matrixB);

        System.out.println(MatrixMath.add(matrixA, matrixB));
        System.out.println(MatrixMath.add(matrixA, matrixB, true));

        Matrix identity3 = Matrix.createIdentityMatrix(3);

        System.out.println(MatrixMath.matrixMultiply(matrixA, matrixB));
        System.out.println(MatrixMath.matrixMultiply(matrixA, identity3));

        System.out.println(MatrixMath.scalarMultiply(matrixA, 5));

        double[][] sourceC = { {1, 2, 3}, {7, 8, 9} };
        Matrix transposeMatrix = new Matrix(sourceC);
        System.out.println(MatrixMath.transpose(transposeMatrix));

        double[] sourceVector = {1, 2, 3, 4, 5};
        Matrix rowMatrix = Matrix.createRowMatrix(sourceVector);
        Matrix colMatrix = Matrix.createColumnMatrix(sourceVector);
        System.out.println("" + rowMatrix.isVectorMatrix() + colMatrix.isVectorMatrix());
        System.out.println("" + MatrixMath.dotProduct(rowMatrix, colMatrix));
    }

}
