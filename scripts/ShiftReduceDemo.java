import edu.stanford.nlp.util.logging.Redwood;

import java.io.StringReader;
import java.util.List;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.shiftreduce.ShiftReduceParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Label;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.Word;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;

//import edu.stanford.nlp.trees.ud.CoNLLUDocumentReader;
/**
 * Demonstrates how to first use the tagger, then use the
 * ShiftReduceParser.  Note that ShiftReduceParser will not work
 * on untagged text.
 *
 * @author John Bauer
 */
public class ShiftReduceDemo  {

  /** A logger for this class */
  private static Redwood.RedwoodChannels log = Redwood.channels(ShiftReduceDemo.class);
  public static void main(String[] args) {
    String modelPath = "edu/stanford/nlp/models/srparser/englishSR.ser.gz";
    String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";
/*
    for (int argIndex = 0; argIndex < args.length; ) {
      switch (args[argIndex]) {
        case "-tagger":
          taggerPath = args[argIndex + 1];
          argIndex += 2;
          break;
        case "-model":
          modelPath = args[argIndex + 1];
          argIndex += 2;
          break;
        default:
          throw new RuntimeException("Unknown argument " + args[argIndex]);
      }
    }
*/
    String text = "My dog likes to shake his stuffed chickadee toy.";

    MaxentTagger tagger = new MaxentTagger(taggerPath);
    ShiftReduceParser model = ShiftReduceParser.loadModel(modelPath,"-originalDependencies");
    TreebankLanguagePack tlp = model.getOp().langpack();
    GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();


    DocumentPreprocessor tokenizer = new DocumentPreprocessor(args[0]);
    System.out.println(tokenizer);
    //print
    TreePrint tp = new TreePrint("conll2007",tlp);
    FileWriter  fw      = null;
     try {
         fw = new FileWriter("testFile-2.txt");
     }catch(IOException e){
         e.printStackTrace();
     }
	PrintWriter printWriter = new PrintWriter(fw);


    int sentece_num = 0;
    int word_num = 0;
    double totalTime = 0;
    for (List<HasWord> sentence : tokenizer) {
      sentece_num += 1;
      List<TaggedWord> tagged = tagger.tagSentence(sentence);
      word_num += tagged.size();
    long start_time = System.nanoTime();
      Tree tree = model.apply(tagged);
	long end_time = System.nanoTime();
	totalTime += end_time - start_time;
      tree.pennPrint();
      System.out.println();
      GrammaticalStructure gs = gsf.newGrammaticalStructure(tree);
      List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();

      System.out.println(tdl);
      tp.printTree(tree,printWriter);
	  //System.out.println();
      //log.info(tree);
    }

    double second = (totalTime/1000000000.0);
    System.out.println("Parse "+Integer.toString(word_num)+" words in " + Integer.toString(sentece_num)+"sentences");

    System.out.print("words/sec: ");
   	System.out.println(word_num/second);
   	System.out.print("setence/sec: ");
   	System.out.println(sentece_num/second);

   	/*
    // You can also use a TreePrint object to print trees and dependencies
    TreePrint tp = new TreePrint("penn,typedDependenciesCollapsed,conll2007");
    tp.printTree(parse);
  }
   	*/

  }
}