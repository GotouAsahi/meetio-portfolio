export const langlist = [
  { name: "C", value: "c" },
  { name: "Cpp", value: "cpp" },
  { name: "Dart", value: "dart" },
  { name: "Go", value: "go" },
  { name: "Java", value: "java" },
  { name: "Javascript", value: "javascript" },
  { name: "Perl", value: "perl" },
  { name: "Php", value: "php" },
  { name: "Python3", value: "python" },
  { name: "R", value: "r" },
  { name: "Ruby", value: "ruby" },
  { name: "Swift", value: "swift" },
  { name: "Typescript", value: "typescript" }
];

export const langSearchlist = ["C", "Cpp", "Dart", "Go", "Java", "Javascript", "Perl", "Php", "Python3", "R", "Ruby", "Swift", "Typescript"];

export const templateList = [
  {
    language: "c",
    text: `#include < stdio.h >
int main(void) {
    printf("Hello World");
    return 0;
}`
  },
  {
    language: "cpp",
    text: `#include < iostream >
using namespace std;
int main(void) {
    cout << "Hello World";
    return 0;
}`
  },
  {
    language: "dart",
    text: `void main() {
    print('Hello, World!');
}`
  },
  {
    language: "go",
    text: `package main
import "fmt"
func main(){
    fmt.Println("Hello World");
}`
  },
  {
    language: "java",
    text: `// ClassはMainにしてください
import java.util.*;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`
  },
  {
    language: "javascript",
    text: `console.log("Hello World")`
  },
  {
    language: "perl",
    text: `print "Hello World";`
  },
  {
    language: "php",
    text: `<?php
    echo "Hello World";
?>`
  },
  {
    language: "python",
    text: `print("Hello, World!")`
  },
  {
    language: "r",
    text: `cat("Hello World")`
  },
  {
    language: "ruby",
    text: `puts "Hello World";`
  },
  {
    language: "swift",
    text: `print("Hello, World!")`
  },
  {
    language: "typescript",
    text: `console.log("Hello World")`
  },
];