# Computational Genomics and Bioinformatics

## 프로젝트 설명
주제를 정하고 주제의 가설을 뒷받침 할수 있도록 DNA와 GeneBank, TaxBrowser 등을 활용하여 증명하는 프로젝트.  

주제: 뱀은 유전적으로 도마뱀과 뱀장어중 어느쪽에 더 가까울까?  


증명과정.  
1. GeneBank를 통해 하나의 뱀 종류를 선택 후, 필요한 정보를 추출. (DNA Sequence, Scientific name, Protein codes, ...)
2. 위에서 얻은 뱀의 단백질타입 (Cytochrome b, Cyclooxygenase 1) 시퀀스를 통해 가장 비슷한 단백질을 가진 5마리의 동물을 도출.
3. Matlab을 통해서 2번의 결과로 얻은 5마리 동물들의 Rooted Phylogenetic Tree를 생성.
4. 뱀장어와 도마뱀 또한 뱀 정보를 찾은 방법으로 추출 후 Tree에 추가.
5. Amino Acid, Nucliotide Sequence에 따른 단백질 두개의 종류를 뱀장어, 도마뱀 각각의 RNA sequence 와 비교분석. 
6. TaxBrowser에서 뱀, 뱀장어, 도마뱀의 조상도를 추출후, 위에서 얻은 결과와 비교.
7. Matlab을 통해 sequcne 분석모델중 하나인 multiple alignment로 확인 후 가설을 정립.
8. 다른 방법론을 사용해 분석한 논문들을 직접 찾아보고 참고후 현재의 프로젝트에 인용 및 결론 도출.

증명과정을 통해 뱀과 뱀장어, 도바뱀은 서로 상당히 근접한 조상을 따르고 있습니다.  
하지만 분석결과 뱀과 도마뱀이 조금더 가까운 조상으로부터 유전을 공통으로 물려받았을 확률이 더 크다고 나왔습니다.  
또한, 제 주장을 뒷받침하기 위해 다른 신뢰도높은 논문들로부터 비슷한 결과를 찾아냈습니다.  


따라서 논문의 결론으로 '뱀은 뱀장어보다 도마뱀과 더 비슷한 유전을 가지고 있다' 를 도출 해 냈습니다.  

## 주요 업무
이번 프로젝트에서 주요 업무로,  
 * Nucleotide BLAST 를 활용해 각 DNA sequence 들을 비교분석
 * 동물 DNA정보를 추출 및 분석
 * DNA 분석 알고리즘 활용하여 비교분석  
 
## 사용 기술
다양한 분석모델을 적용하기 위한 Matlab  
동물들의 몇가지 단백질 시퀀스를 분석하기 위해 BLAST  
