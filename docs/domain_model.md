# Domain Model and Mathematical Formalization (Fintech AI Pipeline)

## 1. Mathematical Model and Loss Function
To evaluate the performance of predictive models in the fintech sector, we optimize the target latency metric and minimize the risks of failures. The loss function $\mathcal{L}$ is defined as follows:

\begin{equation}
    \mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^{N} \left( y_i - \hat{y}_i(\theta) \right)^2 + \lambda \cdot \mathcal{R}(\theta)
\end{equation}

where $\mathcal{R}(\theta)$ is the model complexity regularizer, which prevents overfitting under high-frequency transaction streams.

## 2. Key Latency Percentiles
The $p$-th latency percentile metric $\mathcal{L}_{\text{p}}$ is calculated as:
\begin{equation}
    \mathcal{L}_{\text{p}} = \inf \left\{ t \mid P(T \le t) \ge \frac{p}{100} \right\}
\end{equation}