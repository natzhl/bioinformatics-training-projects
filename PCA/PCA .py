#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from sklearn import decomposition
from matplotlib import pyplot as plt
import altair as alt


# In[4]:


df = pd.read_csv('/home/natali/PCA/matrix.csv')
df


# In[5]:


df.rename(columns={'Unnamed: 0' : 'Sample'}, inplace=True)
df


# In[6]:


non_snp_columns = ['Population code', 'Sample']


# In[7]:


df_snps = df.drop(non_snp_columns, axis=1)
matrix = df_snps.to_numpy()
print(matrix.shape)
matrix


# In[8]:


pca = decomposition.PCA(n_components=2)
pca.fit(matrix)


# In[9]:


print(pca.explained_variance_ratio_)
print(pca.singular_values_)


# In[10]:


to_plot = pca.transform(matrix)
to_plot


# In[11]:


plt.scatter(x=to_plot[:, 0], y=to_plot[:, 1])


# In[12]:


df_plot = df[non_snp_columns].copy()
df_plot


# In[13]:


df_plot['PC1'] = to_plot[:, 0]
df_plot['PC2'] = to_plot[:, 1]
df_plot


# In[14]:


alt.Chart(df_plot).mark_point().encode(
    x='PC1',
    y='PC2',
    color=alt.Color('Population code', scale=alt.Scale(scheme='category20'))
)


# In[15]:


pop = pd.read_csv('/home/natali/PCA/igsr_populations.tsv', sep='\t')
pop


# In[16]:


df_plot = df_plot.merge(pop, on='Population code', how='inner')
df_plot


# In[17]:


alt.Chart(df_plot).mark_point().encode(
    x='PC1',
    y='PC2',
    color=alt.Color('Superpopulation name', scale=alt.Scale(scheme='category20')),
    fill = 'Population code'
)


# ## tSNE

# In[18]:


from sklearn.manifold import TSNE


# In[19]:


X = matrix
X_embedded = TSNE(n_components=2, learning_rate='auto',
                 init='random').fit_transform(X)
X_embedded.shape


# In[20]:


df_plot['tsne1'] = X_embedded[:,0]
df_plot['tsne2'] = X_embedded[:,1]


# In[21]:


df_plot


# In[22]:


alt.Chart(df_plot).mark_point().encode(
    x='tsne1',
    y='tsne2',
    color=alt.Color('Superpopulation name', scale=alt.Scale(scheme='category20'))
)


# In[23]:


alt.Chart(df_plot).mark_point().encode(
    x='tsne1',
    y='tsne2',
    color=alt.Color('Population code', scale=alt.Scale(scheme='category20'))
)


# In[ ]:




