import numpy as np
import matplotlib.pyplot as plt
from imageio import imread
from sklearn.cluster import MiniBatchKMeans

def add_gaussian_noise(im,prop,varSigma):
    N = int(np.round(np.prod(im.shape)*prop))
    index = np.unravel_index(np.random.permutation(np.prod(im.shape))[1:N],im.shape)
    e = varSigma*np.random.randn(np.prod(im.shape)).reshape(im.shape)
    im2 = np.copy(im).astype('float')
    im2[index] += e[index]
    return im2

def add_saltnpeppar_noise(im,prop):
    N = int(np.round(np.prod(im.shape)*prop))
    index = np.unravel_index(np.random.permutation(np.prod(im.shape))[1:N],im.shape)
    im2 = np.copy(im)
    im2[index] = 1-im2[index]
    return im2

def neighbours(i,j,M,N,size=8):
    if size==4:
        if (i==0 and j==0):
            n=[(0,1), (1,0)]
        elif i==0 and j==N-1:
            n=[(0,N-2), (1,N-1)]
        elif i==M-1 and j==0:
            n=[(M-1,1), (M-2,0)]
        elif i==M-1 and j==N-1:
            n=[(M-1,N-2), (M-2,N-1)]
        elif i==0:
            n=[(0,j-1), (0,j+1), (1,j)]
        elif i==M-1:
            n=[(M-1,j-1), (M-1,j+1), (M-2,j)]
        elif j==0:
            n=[(i-1,0), (i+1,0), (i,1)]
        elif j==N-1:
            n=[(i-1,N-1), (i+1,N-1), (i,N-2)]
        else:
            n=[(i-1,j), (i+1,j), (i,j-1), (i,j+1)]
        return n
    if size==8:
        n = []
        if i > 0:
            n.append((i-1,j))
            if j > 0:
                n.append((i-1,j-1))
            if j < N-1:
                n.append((i-1,j+1))
        if j > 0:
            n.append((i,j-1))
        if j < N-1:
            n.append((i,j+1))
        if i < M-1:
            n.append((i+1,j))
            if j > 0:
                n.append((i+1,j-1))
            if j < N-1:
                n.append((i+1,j+1))
        return n

def make_grayscale_plots(imgs):
    fig = plt.figure()
    for i in range(len(imgs)):
        ax = fig.add_subplot(1,len(imgs),i + 1)
        ax.imshow(imgs[i],cmap='gray')
    return fig

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def likelihood(y, x, func_opt='tanh'):
    if func_opt == 'linear':
        if x == 1:
            return 0.1 + 0.8 * y
        else:
            return 0.9 - 0.8 * y
    elif func_opt == 'tanh':
        return 0.5 + 0.5 * x * np.tanh(2 * y - 1.0)
    else:
        raise ValueError('no likelihood function ' + func_opt + ' defined')

def to_grayscale(r,g,b):
    return int(0.2126 * r + 0.7152 * g + 0.0722 * b)

def segment_likelihood(y_bin, fg_hist, bg_hist, x):
    if x == 1:
        # foreground
        return np.tanh(fg_hist[y_bin])
    else:
        return np.tanh(bg_hist[y_bin])

def icm(y, h, beta, eta):
    T = 20

    # initialise x to y
    x = np.copy(y).astype('int')
    ni, nj = x.shape
    for i in range(ni):
        for j in range(nj):
            x[i][j] = (1 if y[i][j] > 0.5 else -1)

    for t in range(T):
        changed = False
        for i in range(ni):
            for j in range(nj):
                e_local_1 = ( h * x[i][j]
                    - beta * sum(1 * ([x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj,size=8)]), 0)
                    #- eta * 1 * (1 if (y[i][j] > 0.5) else -1) )
                    - eta * 1 * 2 * (y[i][j] - 0.5))
                e_local_2 = ( h * x[i][j]
                    - beta * sum(-1 * ([x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj,size=8)]),0)
                    #- eta * -1 * (1 if y[i][j] > 0.5 else -1) )
                    - eta * (-1) * 2 * (y[i][j] - 0.5) )
                before = x[i][j]
                if e_local_1 < e_local_2:
                    x[i][j] = 1
                else:
                    x[i][j] = -1
                if x[i][j] != before:
                    changed = True
        if not changed:
            print('no change after', t,'iterations')
            break
    return x

def gibbs(y, T=1000, randpick=True, w=0.125):
    x = np.copy(y).astype('int')
    ni, nj = x.shape
    for i in range(ni):
        for j in range(nj):
            x[i][j] = (1 if y[i][j] > 0.5 else -1)

    for t in range(T):
        if randpick:
            i = np.random.randint(0,ni)
            j = np.random.randint(0,nj)

            p_numerator = (likelihood(y[i][j], 1)) * np.exp(w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)]))
            p_denominator = ((likelihood(y[i][j], 1)) * np.exp(w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)])) 
                + (likelihood(y[i][j], -1)) * (1 - np.exp(w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)]))) )
            p_ratio = p_numerator / p_denominator
            if p_ratio > np.random.rand():
                x[i][j] = 1
            else:
                x[i][j] = -1
        else:
            for i in range(ni):
                for j in range(nj):                    
                    p_numerator = (likelihood(y[i][j], 1)) * np.exp(w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)])) 
                    p_denominator = ((likelihood(y[i][j], 1)) * np.exp(w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)])) 
                        + (likelihood(y[i][j], -1)) * np.exp(-1 * w * sum([ x[xy[0]][xy[1]] for xy in neighbours(i,j,ni,nj)])) )
                    p_ratio = p_numerator / p_denominator
                    if p_ratio > np.random.rand():
                        x[i][j] = 1
                    else:
                        x[i][j] = -1
    return x

def varia_bayes(y, T=10, w=0.125):
    x = np.copy(y).astype('int')
    mu = np.array(x).astype('float')
    ni, nj = x.shape
    for i in range(ni):
        for j in range(nj):
            x[i][j] = (1 if y[i][j] > 0.5 else -1)
            mu[i][j] = (y[i][j] - 0.5) * 2

    for t in range(T):
        for i in range(ni):
            for j in range(nj):
                m = sum([ w * mu[ij[0]][ij[1]] for ij in neighbours(i,j,ni,nj) ])
                mu[i][j] = np.tanh(m + 0.5 * (likelihood(y[i][j], 1) - likelihood(y[i][j], -1)))
    
    for i in range(ni):
        for j in range(nj):
            # x[i][j] = 1 if mu[i][j] > 0 else -1
            m = sum([ w * mu[ij[0]][ij[1]] for ij in neighbours(i,j,ni,nj) ])
            x[i][j] = 1 if sigmoid(2*(m + 0.5 * (likelihood(y[i][j], 1) - likelihood(y[i][j], -1)))) > 0.5 else -1
    return x

def segmentation(y, im_fg, im_bg, T=10, w=0.125):
    N_BINS = 20

    ni, nj, _ = y.shape

    x = np.zeros((ni,nj))
    mu = np.zeros((ni,nj))

    # bins
    bins = MiniBatchKMeans(N_BINS).fit_predict(y.reshape((ni*nj,3))).reshape((ni,nj))
    
    # histogram
    fg = np.zeros(N_BINS)
    fg_total = 0
    bg = np.zeros(N_BINS)
    bg_total = 0

    for i in range(ni):
        for j in range(nj):
            if im_fg[i][j] > 0:
                fg[bins[i][j]] += 1
                fg_total += 1
            if im_bg[i][j] > 0:
                bg[bins[i][j]] += 1
                bg_total += 1
    
    fg_hist = fg / fg_total
    bg_hist = bg / bg_total

    for i in range(ni):
        for j in range(nj):
            x[i][j] = 1 if np.random.rand() > 0.5 else -1
            mu[i][j] = np.random.randn()

    for t in range(T):
        for i in range(ni):
            for j in range(nj):
                m = sum([ w * mu[ij[0]][ij[1]] for ij in neighbours(i,j,ni,nj) ])
                mu[i][j] = np.tanh(m + 0.5 * (segment_likelihood(bins[i][j],fg_hist,bg_hist,1) - segment_likelihood(bins[i][j],fg_hist,bg_hist, -1)))
    
    for i in range(ni):
        for j in range(nj):
            x[i][j] = 1 if mu[i][j] > 0 else -1
    return x

# proportion of pixels to alter

# prop = 0.7
# varSigma = 0.5
# im = imread('lena-bw.gif')
# im = imread('shiki-bw.png')
# im = imread('pug2.jpg')

# im = imread('shiki-colour-resized.png')[:,:,:3]
im = imread('shiki-colour.png')[:,:,:3]
im_mask = imread('shiki-colour-mask.png')[:,:,:3]

nx,ny,_ = im.shape

im_fg = np.zeros((nx,ny))
im_bg = np.zeros((nx,ny))

print(nx,ny)

for i in range(nx):
    for j in range(ny):
        p = im_mask[i][j]
        r = p[0]
        g = p[1]
        b = p[2]
        if r == 0 and g == 0 and b == 0:
            im_bg[i][j] = 1
        elif r == 255 and g == 255 and b == 255:
            im_fg[i][j] = 1

# im = imread('pug4.jpg')[:,:,:3]

# im = imread('shiki2.jpg')[:,:,:3]
im_out = np.copy(im)



im_seg = segmentation(im,im_fg, im_bg)

ni,nj,_ = im_out.shape
for i in range(ni):
    for j in range(nj):
        for k in range(3):
            im_out[i][j][k] = im[i][j][k] * (1 if im_seg[i][j] > 0 else 0)

fig = plt.figure()
ax = fig.add_subplot(1,3,3)
ax.imshow(im_out)
ax2 = fig.add_subplot(1,3,1)
ax2.imshow(im)
ax3 = fig.add_subplot(1,3,2)
ax3.imshow(im_mask)

# im_gray = np.zeros((ni,nj))
# for i in range(ni):
#     for j in range(nj):
#         im_gray[i][j] = to_grayscale(im[i][j][0],im[i][j][1],im[i][j][2])

# make_grayscale_plots([im_gray])



# make_grayscale_plots([im_out])

# ni,nj = im.shape

# ims = np.sort(im.reshape((-1)))
# # ims = ims.reshape((ni,nj))
# t1 = int(len(ims) / 4)
# t3 = 3 * t1
# im2 = np.copy(im)
# im3 = np.copy(im)
# im4 = np.copy(im)

# for i in range(ni):
#     for j in range(nj):
#         im2[i][j] = 1 if im[i][j] < ims[t1] else 0
#         im3[i][j] = 0 if im[i][j] < ims[t3] else 1
#         im4[i][j] = im2[i][j] * 


# make_grayscale_plots([im,im2,im3,im4])


# im = im/255


# im2 = add_gaussian_noise(im,prop,varSigma)
# im3 = add_saltnpeppar_noise(im,prop)
# im4 = icm(im2, 0.0, 2.0, 4.0)
# im5 = gibbs(im2, T=10, randpick=False, w=0.25)
# im6 = varia_bayes(im2,10)

# images = [im,im2,im4,im5,im6]
# make_grayscale_plots(images)

plt.show()

