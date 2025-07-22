const baseurl = process.env.NODE_ENV === 'production'
  ? 'http://184.73.208.222'
  : 'http://localhost:8000';

export const templatethumbnail = [
  `${baseurl}/media/default/technology_thumbnail.jpg`,
  `${baseurl}/media/default/business_thumbnail.jpg`,
  `${baseurl}/media/default/creative_thumbnail.jpg`,
  `${baseurl}/media/default/sound_thumbnail.jpg`,
  `${baseurl}/media/default/video_thumbnail.jpg`,
  `${baseurl}/media/default/design_thumbnail.jpg`
];

export const templateList = [
  {
    text: `## 作品・成果物
作品や成果物の画像やリンク、説明文などを記載
![image](${baseurl}/media/default/technology_sentence.jpg)

## 制作経緯・制作目的
制作に至った経緯や目的を記載

## 制作過程・期間
制作するにあたって力を入れた点、つまづいた点などを記載

## 使用機材・使用ソフト
使用した機材やソフト、プログラミング言語などを記載

## 参考文献
制作するにあたって参考にした文献を記載`
  },
  {
    text: `## 企画・プロジェクト
企画やプロジェクトの画像やリンク、説明文などを記載
![image](${baseurl}/media/default/business_sentence.jpg)

## 経緯・目的
企画を行うに至った経緯や目的を記載

## 企画過程・プロジェクト過程・期間
企画を進行するにあたって力を入れた点、つまづいた点などを記載

## 担当
企画を進行するにあたって担当したポジションを記載

## 参考文献
企画を進行するにあたって参考にした文献を記載`
  },
  {
    text: `## 作品・成果物
作品や成果物の画像やリンク、説明文などを記載
![image](${baseurl}/media/default/creative_sentence.jpg)

## 制作経緯・制作目的
制作に至った経緯や目的を記載

## 制作過程・期間
制作するにあたって力を入れた点、つまづいた点などを記載

## 使用機材・使用ソフト
使用した機材やソフトなどを記載

## 参考文献
制作するにあたって参考にした文献を記載`
  },
  {
    text: `## 作品・成果物
作品や成果物の音声ファイルやリンク、説明文などを記載
![image](${baseurl}/media/default/sound_sentence.jpg)

## 制作経緯・制作目的
制作に至った経緯や目的を記載

## 制作過程・期間
制作するにあたって力を入れた点、つまづいた点などを記載

## 使用機材・使用ソフト
使用した機材やソフトなどを記載

## 参考文献
制作するにあたって参考にした文献を記載`
  },
  {
    text: `## 作品・成果物
作品や成果物の映像やリンク、説明文などを記載
![image](${baseurl}/media/default/video_sentence.jpg)

## 制作経緯・制作目的
制作に至った経緯や目的を記載

## 制作過程・期間
制作するにあたって力を入れた点、つまづいた点などを記載

## 使用機材・使用ソフト
使用した機材やソフトなどを記載

## 参考文献
制作するにあたって参考にした文献を記載`
  },
  {
    text: `## 作品・成果物
作品や成果物の画像やリンク、説明文などを記載
![image](${baseurl}/media/default/design_sentence.jpg)

## 制作経緯・制作目的
制作に至った経緯や目的を記載

## 制作過程・期間
制作するにあたって力を入れた点、つまづいた点などを記載

## 使用機材・使用ソフト
使用した機材やソフトなどを記載

## 参考文献
制作するにあたって参考にした文献を記載`
  }
]