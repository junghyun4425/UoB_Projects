# Machine Learning

## 프로젝트 설명

### Coursework 1
Linear regression, Gaussian Process등의 모델을 분석 후 설명, 실제로 구현.  
지도학습 과 비지도학습을 각각 모델링.  
모든 이론과 실습은 Bayesian concept을 기초로 하여 진행됩니다.  
Prior, Posterior, Likelihood, Evidence와 같이 오래된 수학이론을 실제 모던 머신러닝에 적용하여 진행.  

### Coursework 2
Inference 알고리즘을 통해 노이즈를 다양한 관점에서 추론하여 제거하는 모델 구현.  


상세내용
 * Iterative Conditional Modes (ICM) 실제 구현 및 이미지 노이즈 필터로 사용.
 * Gibbs Sampling model 구현 및 샘플링을 통해 노이즈 필터 성능을 향상시킴.
 * Ising model을 다양한 관점에서 확장시킨 후(Mean field approximation, Variational Bayes), 노이즈 필터에 최적의 성능을 내도록 구현.
 * 더 나아가 유색 이미지파일의 배경과 물체를 구분하는 모델 구현 (Image Segmentation) - 기존의 모델에서 latent value를 이용하여 배경, 물체구분 후 두개의 Histogram을 통해 물체를 추출.
 * MNIST 데이터를 사용해 구현된 Variational Auto-encoder를 Tensorflow를 통해 수행후 분석. 
