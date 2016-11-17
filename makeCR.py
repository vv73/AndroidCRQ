from xml.dom import minidom
elements = []

def add_element(element):
    global elements
    for elem in elements:
        if elem["tag"] == element["tag"] and "attr: name" in elem and "attr: name" in element and elem["attr: name"] == element["attr: name"]:
                return
    elements.append(element)

def parse_node(node, filename, level):
    global elements;
    if node.nodeType == node.ELEMENT_NODE:
        element = {}
        element["tag"] = node.tagName
        if level == 0:
            element["attr: name"] = filename
        element["value"] = filename
        element["childs"] = [] 
        for (name, value) in node.attributes.items():
            element["attr: " + name] = value
                              
        if node.childNodes:
            for child in node.childNodes:
               if child.nodeType == child.TEXT_NODE:
                    element["value"] = child.wholeText.strip()
                     
               if child.nodeType == child.ELEMENT_NODE:
                   n = parse_node(child,filename, level + 1)
                   element["childs"].append(n)
        add_element(element)
        return len(elements) - 1;
    
def printR():
    global elements
    classStart = "public static final class "
    itemStart = "\n\tpublic static final int "
    ids = classStart + "id" +"{"
    layouts = classStart + "layout" +"{"
    drawables = classStart + "drawable" +"{"
    strings = classStart + "string" +"{"
    styles = classStart + "style" +"{"
    attrs = classStart + "attr" +"{"
    print("""import java.util.HashMap;
public class CR{
       	public static class AttrHashMap extends HashMap<String, String> {
		AttrHashMap putAttr(String key, String value) {
			super.put(key, value);
			return this;
		}
	}

	public static class Res {
		String type;
		HashMap<String, String> attrs;
		String value;
		int[] childs;

		public Res(String type, String value, int[] childs, AttrHashMap attrs) {
			this.type = type;
			this.attrs = attrs;
			this.value = value;
			this.childs = childs;
		}
	}""");
    i = 0;
    for element in elements:
        if "attr: android:id" in element:
            ids += itemStart + element["attr: android:id"][5:] + "=" + hex(i) + ";";
        if element["tag"] == "string":
            strings += itemStart + element["attr: name"] + "=" + hex(i) +";";
        if element["tag"] == "drawable":
             drawables += itemStart + element["attr: name"][:-4] + "=" + hex(i) + ";";
        if element["tag"] == "style":
            styles += itemStart + element["attr: name"] + "=" + hex(i) + ";";
        if "attr: name" in element and element["attr: name"].startswith("layout:"):
            layouts += itemStart + element["attr: name"][7:-4] + "=" + hex(i) + ";";    
        i += 1;
    print (ids + "\n}\n" + layouts + "\n}\n" + drawables + "\n}\n" + strings +"\n}\n" + styles +"\n}\n" + attrs + "\n}");
    print ("\npublic static final Res[] resourses = new Res[] {", end="")
           
    for element in elements:
        print ("\n\tnew Res(\""+element["tag"] + "\",\"" + element["value"] + "\",new int[]{"+ ",".join(map(str, element["childs"]))+"},", end="")
        print ("new AttrHashMap()", end="")                                                                                                 
        for key in element:
           if key.startswith("attr:"):
                 print(".putAttr(\"" + key[6:] + "\",\"" + element[key] + "\")",  end = "");
        print ("),", end = "")
                  
    
    print ("\n};");
    print ("}");
                   
                     


import sys
import os

#root = sys.argv[1];
root = "C:\\Users\\vv\\\AndroidStudioProjects\\Test\\app\\src\\main\\res"

folders = next(os.walk(root))[1]

for folder in folders:
    files = next(os.walk(root+ "/" + folder))[2]
    for file in files:
        if file.endswith(".jpg") or file.endswith(".gif") or file.endswith(".png"):
               element = {}
               element["tag"]= "drawable"
               element["childs"] = []
               element["attr: name"] = element["value"] = file
               add_element(element)
        if file.endswith(".xml"):
           xmldoc = minidom.parse(root+"/"+folder+"/"+file).documentElement
           parse_node(xmldoc, folder+":"+file, 0);
           
sys.stdout = open('CR.java', 'w')
printR()
sys.stdout.close()            

