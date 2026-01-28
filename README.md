# Multi-Stakeholder Equilibrium Recommender

A novel recommendation framework that moves beyond simple Click-Through Rate (CTR) maximization. This system optimizes for **Social Welfare**, balancing the competing needs of Users, Content Creators, the Platform, and Society at large.

## 🌟 The Problem

Modern recommender systems (YouTube, TikTok, Facebook) are often optimized solely for **User Engagement** or **Relevance**. While this creates addictive products, it creates negative externalities:

* **The "Rich Get Richer":** Popular creators dominate, leaving new creators with zero exposure.
* **Filter Bubbles:** Users are only shown what they already like, reducing diversity.
* **Societal Harm:** Polarizing or misleading content is promoted because it generates engagement.

## 🚀 The Solution

This project implements a **Social Welfare Function** to select recommendation slates. It treats recommendation as a multi-objective optimization problem where:

1. **User Utility:** High relevance, high satisfaction.
2. **Creator Utility:** Fair exposure (opportunity for new/less popular items).
3. **Platform Utility:** High engagement and retention.
4. **Society Utility:** Low misinformation, low polarization.

### The Algorithm

We generate $N$ random candidate slates and evaluate the "Social Welfare" $W$ of each slate:

$$
W(s) = \sum_{i \in \{User, Creator, Platform, Society\}} U_i(s) - P_{rawlsian}
$$

Where $P_{rawlsian}$ is a penalty applied if the utility of any single stakeholder drops below a threshold relative to the group average. This ensures that we do not maximize total welfare at the total expense of one group (e.g., sacrificing Society to boost User engagement).

## 📊 Dataset

This project uses the **MovieLens Small Dataset** (real-world data).

* **Relevance:** Derived from average movie ratings.
* **Engagement:** Derived from rating counts.
* **Exposure:** Inverse of popularity (boosting niche movies).
* **Societal Risk:** Simulated "controversy" scores assigned to movies (since MovieLens does not contain political data).

## 🛠️ Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install numpy pandas matplotlib seaborn requests
```

## 💻 Usage

Run the benchmark to compare the **Equilibrium Recommender** against a standard **Greedy User-Centric Recommender**.

```bash
python main.py
```

This will:

1. Download and process MovieLens data.
2. Generate 1,000 random recommendation slates.
3. Select the best slate using the Equilibrium algorithm vs. a Greedy approach.
4. Output a text report.
5. Generate `advanced_recommender_benchmark.png` with visual comparisons.

## 📈 Results

The algorithm generates a dashboard containing:

1. **Performance Metrics:** Bar charts comparing Relevance, Diversity, Exposure, and Risk scores.
2. **Stakeholder Radar Chart:** Visualizing the "Pareto Frontier" of utility balance.
3. **Risk vs. Relevance Scatter Plot:** Showing which items were selected by each algorithm and how they trade off safety for quality.

### Typical Outcome

* **Greedy Approach:** Maximizes Relevance but often picks high-risk (controversial) items and offers zero exposure to new creators.
* **Equilibrium Approach:** Slightly lowers raw Relevance to drastically reduce Misinformation and increase Creator Fairness, resulting in a healthier system state.

## 📝 Core Logic

The optimization logic is decoupled from the data loading in `core_logic.py`. To integrate this into your own system:

```python
from core_logic import MultiStakeholderRecommender, StakeholderUtility

# Define your stakeholders
stakeholders = [
    StakeholderUtility('User', {'relevance': 1.0, 'diversity': 0.2}),
    StakeholderUtility('Society', {'misinformation': -2.0})
]

# Initialize
rec = MultiStakeholderRecommender(stakeholders)

# Select from candidates
best_result = rec.select_optimal_slate(my_candidate_slates)
```

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Areas of interest:

* Better Pareto-frontier search algorithms (e.g., Genetic Algorithms instead of random sampling).
* Real-world integration of content safety APIs.
* User study A/B testing frameworks.
