# 4. Experiment Results & Discussion

This section presents an empirical evaluation of the proposed fintech pipeline architecture. We analyze execution latencies, extreme tail behavior ($p_{95}, p_{99}$), error rate guardrails, and system resource utilization under varying request load intensities.

## 4.1. Mathematical Performance Model

To formally evaluate system performance, we model execution latency distribution percentiles. The $p$-th percentile latency $\mathcal{L}_{\text{p}}$ is defined as:

\begin{equation}
    \mathcal{L}_{\text{p}} = \inf \left\{ t \mid P(T \le t) \ge \frac{p}{100} \right\}
\end{equation}

To quantify performance gains, the relative speedup $S$ of the optimized architecture compared to the baseline is calculated as:

\begin{align}
    S &= \frac{\underbrace{T_{\text{baseline}}}_{\text{Baseline execution time}}}{\underbrace{T_{\text{optimized}}}_{\text{Optimized execution time}}} 
    = \frac{\frac{1}{N}\sum_{i=1}^{N} t_{i}^{(\text{base})}}{\frac{1}{M}\sum_{j=1}^{M} t_{j}^{(\text{opt})}},
\end{align}

where uncertainty and confidence bounds are evaluated using a 95% bootstrap confidence interval:

\begin{equation}
    \text{CI}_{95\%} = \left[ \hat{\theta}^*_{(0.025 \cdot B)}, \hat{\theta}^*_{(0.975 \cdot B)} \right]
\end{equation}

---

## 4.2. Comparative Performance Analysis

Table 1 summarizes the core performance metrics across different system architectures under a steady workload of 500 RPS. The results demonstrate that the optimized studio pipeline significantly reduces both median and tail latencies while maintaining a zero-error rate.

**Table 1:** Performance and Tail Latency Comparison across Pipeline Variants under 500 RPS Load.

| System Architecture | Throughput [req/s] | Latency $p_{50}$ [ms] | Tail $p_{95}$ [ms] | Error Rate [\%] |
| :--- | :---: | :---: | :---: | :---: |
| Baseline Monolith | $412 \pm 24$ | $45.2 \, (38.1\text{--}52.4)$ | $118.5$ | $2.14$ |
| Async Reactive Engine | *$785 \pm 31$* | *$22.4 \, (18.6\text{--}26.8)$* | *$64.2$* | *$0.42$* |
| **Optimized Studio (Ours)** | **$940 \pm 18$** | **$14.1 \, (11.9\text{--}16.5)$** | **$31.0$** | **$0.00$** |

---

## 4.3. Latency Scaling and Guardrail Evaluation

Figure 1 illustrates the execution scaling profile and tail variability across request load intensities ranging from 100 to 1000 RPS. 

* (a) Median ($p_{50}$) and extreme tail ($p_{95}, p_{99}$) latencies exhibit sub-linear growth up to 750 RPS, followed by graceful saturation.
* (b) The guardrail error rate remains strictly below the 1.0% safety threshold across operational states.
* (c) CPU and resource utilization scales predictably under heavy loads.

> **Fig. 1:** Execution latency scaling profile and tail variability across request load intensities (100–1000 RPS). Shaded regions indicate interquartile ranges (IQR, $p_{25}\text{--}p_{75}$) derived from $N=1000$ independent benchmark runs with 95% bootstrap confidence intervals.