package genericSearching;
import java.util.AbstractMap;
import java.util.Comparator;
import java.util.Iterator;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;
public class StudentSearch2{
    @SuppressWarnings("resource")
    public static void main( String [ ] args ) {//テスト用のmainメソッド
        
        //データ型がStudentData型である空の2分探索木treeを作る
        VisitableBinSearchTree2<Integer,String> tree =
            new VisitableBinSearchTree2<Integer,String>(
                //new VisitableBinSearchTree2<Integer,String>によりインスタンス化されると同時に、
                //以下のComparatorもnew演算子によってインスタンス化される。
                //このComparatorインスタンスは VisitableBinSearchTree2 のコンストラクタの引数として渡される
                new Comparator<Integer>() {
                    //オーバーライド
                    public int compare(Integer a, Integer b) {
                        return a - b ;
                    }
                }
            ) ;
        
        //nをキーボードから入力して、1,2,...,nの順列をランダムに作る
        int n ;
        Scanner keyboard = new Scanner(System.in) ;
        System.out.println("#students:") ;
        n = keyboard.nextInt();
        int[] array = new int[n] ;
        for (int i = 0 ; i < n ; i++)
            array[i] = i + 1;
        Random rand = new Random() ;
        for (int i = 0 ; i < n ; i++) {
            int j = rand.nextInt(n - i) ;
            int temp = array[n - 1 - i] ;
            array[n - 1 - i] = array[j] ;
            array[j] = temp ;
        }
        
        //キーが1,2,...,ｎのデータを上で作った順番にtreeに挿入する
        for (int i = 0 ; i < n ; i++) {
            //＜AbstractMapの説明＞
            //java.utilパッケージのクラスの一つ。
            //AbstractMap.SimpleEntry<Integer,String> は、単なるキーと値のペアを表すクラスであり、
            //特定のメソッドの戻り値として固定された型を持つものではない。データの一時的な保存や操作に使用される。
            
            //＜<Integer,String>について＞
            //<Integer, String> は整数型のキーと文字列型の値を持つ一般的なデータ構造やクラスを示す。
            //このようなデータ構造は、キーと値のペアを保持し、異なる型のデータを格納できる柔軟性を
            //提供する。例えば、Map<Integer, String> は整数型のキーと文字列型の値を持つマップを
            //表す。
            tree.insert(new AbstractMap.SimpleEntry<Integer,String>(array[i], i + "-th string"));
        }
        System.out.println("") ;

        ここまでやった
        //treeの高さを求める
        tree.accept(new BTVisitor<Integer,String>() {
            public Integer visitNull( ) {
                return 0 ;
            }
            public Integer visitNode(Object left, Object right, Map.Entry<Integer,String> data) {
                return Math.max((Integer)left, (Integer)right) + 1 ;
            }
        });
        System.out.println("height: " + (Integer)tree.traverse());
        System.out.println("") ;
        
        //treeをpostorder順にたどって、データを表示
        System.out.println("visiting the tree in post order");
        tree.accept(new BTVisitor<Integer,String>() {
            public Void visitNull( ) {
                return null ;
            }
            public Void visitNode(Object left, Object right, Map.Entry<Integer,String> data) {
                System.out.println(data.getKey() + ":" + data.getValue());
                return null ;
            }
        });
        tree.traverse();
        System.out.println("") ;
        
        //検索と削除操作をテストする
        int m = rand.nextInt(n) ;
        System.out.println("trying to find " + m + " ...");
        String result = tree.search(m) ;
        if (result != null) {
            System.out.println("found " + m + ":" + result) ;
            System.out.println("") ;
            System.out.println("trying to delete " + m + " ...");
            tree.delete(m);
            result = tree.search(m) ;
            if (result != null)
                System.out.println("Error: found the deleted data.") ;
        }
        System.out.println("") ;
        Iterator<Map.Entry<Integer,String>> iter = tree.inorderIterator() ;
        System.out.println("data in sorted order:");
        while (iter.hasNext()) {
            Map.Entry<Integer,String> d = iter.next();
            System.out.println(d.getKey() + " F" + d.getValue());
        }
        
        //unbalance度を求める
        tree.accept(new BTVisitor<Integer,String>() {
            int unbalance=0;
            int tmp=0;
            Integer lcount=0;
            Integer rcount=0;
            public Integer visitNull( ) {
                return 0 ;
            }
            
            public Integer visitNode(Object left, Object right, Map.Entry<Integer,String> data) {
                BinSearchTreeNode Root = tree.getRoot();
                Map.Entry originData=Root.getData();
                  originData.getKey();
            if(data.getKey()<(Integer)originData.getKey()){
                lcount++;
            }
            if(data.getKey()>(Integer)originData.getKey()){
                rcount++;
            }
            else{
                lcount=(Integer)left;
                rcount=(Integer)right;
            }
                tmp=lcount-rcount;
                if(tmp<0){
                    tmp=tmp*(-1);
                }
                if(tmp>unbalance){
                    unbalance=tmp;
                }
                //System.out.println("tree's unbalance:"+unbalance);
                return unbalance ;
            }
        });
        
        System.out.println("tree's unbalance:"+(Integer)tree.traverse());
        System.out.println("") ;
    }
}