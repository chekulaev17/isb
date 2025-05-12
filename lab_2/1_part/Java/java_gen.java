import java.util.Random;


public class RandomBinary128 {
    public static void main(String[] args) {

        Random random = new Random();
        StringBuilder binarySequence = new StringBuilder();

        for (int i = 0; i < 128; i++) {
            int bit = random.nextInt(2);
            binarySequence.append(bit);
        }
        System.out.println(binarySequence.toString());
    }
}