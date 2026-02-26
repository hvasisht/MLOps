import os
import re
import pickle
import base64

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Docker
import matplotlib.pyplot as plt


DATA_PATH = "/opt/airflow/data/netflix_titles.csv"
WORKING_DIR = "/opt/airflow/working_data"
MODEL_DIR = "/opt/airflow/model"


def _b64_pickle(obj) -> str:
    """Helper function to serialize and encode objects"""
    return base64.b64encode(pickle.dumps(obj)).decode("ascii")


def _unpickle_b64(s: str):
    """Helper function to decode and deserialize objects"""
    return pickle.loads(base64.b64decode(s))


def load_data():
    """
    Load Netflix dataset from CSV file.
    Returns: Base64 encoded serialized DataFrame
    """
    print("Loading Netflix dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns")
    print("Columns:", df.columns.tolist())

    serialized_data = pickle.dumps(df)
    return base64.b64encode(serialized_data).decode("ascii")


def data_preprocessing(df_b64: str):
    """
    Enhanced preprocessing with additional features.
    
    NEW FEATURES ADDED (Beyond Template):
    1. title_length - Length of movie title
    2. description_length - Length of description text  
    3. num_genres - Number of genres listed
    
    Original Features:
    - release_year
    - duration_min
    - added_year
    
    Returns: Base64 encoded serialized numpy array
    """
    df = _unpickle_b64(df_b64)
    
    print("Starting data preprocessing...")

    # Keep only Movies to make 'duration' consistent (minutes)
    df = df[df["type"].fillna("") == "Movie"].copy()
    print(f"Filtered to {len(df)} movies")

    # Parse duration like "90 min" -> 90
    def parse_minutes(x):
        if pd.isna(x):
            return None
        m = re.search(r"(\d+)", str(x))
        return int(m.group(1)) if m else None

    df["duration_min"] = df["duration"].apply(parse_minutes)

    # Extract year from date_added
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["added_year"] = df["date_added"].dt.year

    # ========== NEW FEATURES (MODIFICATION 1) ==========
    # Feature 1: Length of movie title
    df["title_length"] = df["title"].str.len()
    
    # Feature 2: Length of description
    df["description_length"] = df["description"].fillna("").str.len()
    
    # Feature 3: Number of genres (count commas in 'listed_in' + 1)
    df["num_genres"] = df["listed_in"].fillna("").str.count(",") + 1
    # ===================================================

    # Select ALL features for clustering (6 features total)
    feats = df[["release_year", "duration_min", "added_year", 
                "title_length", "description_length", "num_genres"]].copy()
    
    print(f"Features before dropna: {len(feats)}")
    feats = feats.dropna()
    print(f"Features after dropna: {len(feats)}")
    print(f"Feature columns: {feats.columns.tolist()}")

    # Normalize features using MinMaxScaler
    scaler = MinMaxScaler()
    X = scaler.fit_transform(feats)

    # Save preview for verification
    os.makedirs(WORKING_DIR, exist_ok=True)
    preview_path = os.path.join(WORKING_DIR, "features_preview_50.csv")
    feats.head(50).to_csv(preview_path, index=False)
    print(f"Saved feature preview to: {preview_path}")

    return _b64_pickle(X)


def build_save_model(X_b64: str, filename: str):
    """
    Build K-Means clustering model using elbow method.
    Saves model to file.
    
    Returns: List of SSE values for visualization
    """
    X = _unpickle_b64(X_b64)
    print(f"Building model with {X.shape[0]} samples and {X.shape[1]} features")

    sse = []
    kmeans_kwargs = {"init": "k-means++", "n_init": 10, "max_iter": 300, "random_state": 42}

    # Test k values from 1 to 10
    k_range = range(1, 11)
    print("Calculating SSE for different k values...")
    for k in k_range:
        km = KMeans(n_clusters=k, **kmeans_kwargs)
        km.fit(X)
        sse.append(float(km.inertia_))
        print(f"  k={k}: SSE={km.inertia_:.2f}")

    # Determine optimal k using elbow method
    kl = KneeLocator(list(k_range), sse, curve="convex", direction="decreasing")
    best_k = kl.elbow or 3  # fallback to 3 if elbow not found
    print(f"\n✓ Optimal k determined by elbow method: {best_k}")

    # Train final model with optimal k
    final_model = KMeans(n_clusters=int(best_k), **kmeans_kwargs)
    final_model.fit(X)

    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "wb") as f:
        pickle.dump(final_model, f)

    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Model has {final_model.n_clusters} clusters")

    return sse


def load_model_elbow(filename: str, sse: list):
    """
    Load saved model and verify elbow point.
    
    Returns: Number of clusters in loaded model
    """
    model_path = os.path.join(MODEL_DIR, filename)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")

    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    print(f"✓ Loaded model from: {model_path}")
    print(f"✓ Model uses k = {model.n_clusters} clusters")

    # Verify elbow method result
    k_range = range(1, 11)
    kl = KneeLocator(list(k_range), sse, curve="convex", direction="decreasing")
    print(f"✓ Elbow method confirms optimal k = {kl.elbow}")

    return int(model.n_clusters)


def create_elbow_visualization(sse: list):
    """
    ========== MODIFICATION 2: NEW VISUALIZATION TASK ==========
    Create and save elbow plot for SSE vs number of clusters.
    This helps visualize the optimal k selection.
    
    Returns: Path to saved plot
    """
    print("Creating elbow plot visualization...")
    
    k_range = list(range(1, len(sse) + 1))
    
    # Create figure
    plt.figure(figsize=(10, 6))
    plt.plot(k_range, sse, 'bo-', linewidth=2, markersize=8)
    
    # Identify elbow point
    kl = KneeLocator(k_range, sse, curve="convex", direction="decreasing")
    if kl.elbow:
        plt.axvline(x=kl.elbow, color='r', linestyle='--', linewidth=2, 
                   label=f'Optimal k = {kl.elbow}')
        plt.plot(kl.elbow, sse[kl.elbow-1], 'r*', markersize=20, 
                label='Elbow Point')
    
    # Styling
    plt.xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
    plt.ylabel('Sum of Squared Errors (SSE)', fontsize=12, fontweight='bold')
    plt.title('Elbow Method for Optimal k - Netflix Movie Clustering', 
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=10)
    plt.tight_layout()
    
    # Save plot
    os.makedirs(MODEL_DIR, exist_ok=True)
    plot_path = os.path.join(MODEL_DIR, "elbow_plot.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Elbow plot saved to: {plot_path}")
    return plot_path


def analyze_clusters(filename: str):
    """
    ========== MODIFICATION 3: NEW CLUSTER ANALYSIS TASK ==========
    Analyze cluster characteristics and generate summary statistics.
    
    Returns: Dictionary with cluster analysis results
    """
    print("Analyzing cluster characteristics...")
    
    # Load model
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    # Load preprocessed features
    features_path = os.path.join(WORKING_DIR, "features_preview_50.csv")
    df = pd.read_csv(features_path)
    
    # Normalize features (same as preprocessing)
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df)
    
    # Predict clusters
    df['cluster'] = model.predict(X)
    
    # Calculate statistics for each cluster
    print(f"\n{'='*60}")
    print("CLUSTER ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"Total samples: {len(df)}")
    print(f"Number of clusters: {model.n_clusters}")
    print(f"Features analyzed: {df.columns.tolist()[:-1]}")  # Exclude 'cluster' column
    
    # Cluster size distribution
    cluster_counts = df['cluster'].value_counts().sort_index()
    print(f"\n{'Cluster':<10} {'Count':<10} {'Percentage':<10}")
    print('-' * 30)
    for cluster_id, count in cluster_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{cluster_id:<10} {count:<10} {percentage:<10.1f}%")
    
    # Detailed statistics by cluster
    stats = df.groupby('cluster').agg({
        'release_year': ['mean', 'min', 'max', 'std'],
        'duration_min': ['mean', 'min', 'max', 'std'],
        'added_year': ['mean', 'min', 'max', 'std'],
        'title_length': ['mean', 'min', 'max', 'std'],
        'description_length': ['mean', 'min', 'max', 'std'],
        'num_genres': ['mean', 'min', 'max', 'std']
    }).round(2)
    
    # Save detailed statistics
    stats_path = os.path.join(WORKING_DIR, "cluster_statistics.csv")
    stats.to_csv(stats_path)
    print(f"\n✓ Detailed cluster statistics saved to: {stats_path}")
    
    # Create cluster summary report
    summary_path = os.path.join(WORKING_DIR, "cluster_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("NETFLIX MOVIE CLUSTERING - ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Movies Analyzed: {len(df)}\n")
        f.write(f"Number of Clusters: {model.n_clusters}\n")
        f.write(f"Features Used: {', '.join(df.columns.tolist()[:-1])}\n\n")
        
        f.write("CLUSTER SIZE DISTRIBUTION\n")
        f.write("-" * 60 + "\n")
        for cluster_id, count in cluster_counts.items():
            percentage = (count / len(df)) * 100
            f.write(f"Cluster {cluster_id}: {count} movies ({percentage:.1f}%)\n")
        
        f.write("\n" + "=" * 60 + "\n")
        f.write("CLUSTER CHARACTERISTICS\n")
        f.write("=" * 60 + "\n\n")
        
        for cluster_id in sorted(df['cluster'].unique()):
            cluster_data = df[df['cluster'] == cluster_id]
            f.write(f"\nCluster {cluster_id} Profile:\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Size: {len(cluster_data)} movies\n")
            f.write(f"  Avg Release Year: {cluster_data['release_year'].mean():.0f}\n")
            f.write(f"  Avg Duration: {cluster_data['duration_min'].mean():.0f} minutes\n")
            f.write(f"  Avg Title Length: {cluster_data['title_length'].mean():.0f} characters\n")
            f.write(f"  Avg Description Length: {cluster_data['description_length'].mean():.0f} characters\n")
            f.write(f"  Avg Number of Genres: {cluster_data['num_genres'].mean():.1f}\n")
    
    print(f"✓ Cluster summary report saved to: {summary_path}")
    print(f"{'='*60}\n")
    
    return {
        'num_clusters': int(model.n_clusters),
        'cluster_sizes': cluster_counts.to_dict(),
        'statistics_file': stats_path,
        'summary_file': summary_path
    }