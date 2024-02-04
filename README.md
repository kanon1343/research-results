# 修正後のプログラムの分析

個体生成数のパターン別に分けています。 <br>
以下のようにファイルを管理しています。

```
100-100-50
   ├── codec8-log
       ├── correct_patch0.csv(受理パッチ)
       ├── seed0.txt.csv(kGenProgのログ)
       ├── duplicate_lines_report.csv(繰り返し)
       ├── seed0-info.csv(seedごとの分析結果)
       ├── selection.csv(分類結果)
       └── summary-info.csv(全体のサマリー)
   ├── codec9-log
   ├── math46-log
   ├── math49-log
   ├── math72-log
   ├── math78-log
   ├── math80-log
   ├── math82-log
   ├── math85-log

```

# 分類に使用したもの

- pmd で使用するルール：rule.xml
- 繰り返し行検出：duplicate_search.py

# 修正パッチは量が多いため別リポジトリにあります

(https://github.com/kanon1343/research)
