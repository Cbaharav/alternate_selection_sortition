import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import csv

PLOT_INSTANCE_NAME = {'Petaluma_2022': 'US-2', 'Deschutes_2024': 'US-3', 'Eugene-2020': 'US-1'}
PLOT_DATASET_NAME = {'HD': 'US', 'MASS_ALFD': 'Can'}

def plot_losses_for_dataset(instance_names, all_alt_indices, upper_bound, lower_bound, losses, loss_labels, ks, filename, true_prac_losses = None, loss_type = 'l1', with_stddev = True):
    num_instances = len(instance_names)
    fig, axes = plt.subplots(1, num_instances, figsize=(15, 6), sharey=True)

    for i, instance_name in enumerate(instance_names):
        alt_indices = all_alt_indices[instance_name]
        inst_loss = losses[instance_name]
        ax = axes[i]
        if 'L1 Opt' in loss_labels:
            colors = {
                'L1 Opt': '#A020F0', # purple
                'Binary Opt': '#FFA500',         # Bright orange
                'Practitioner': '#2ca02c',         # Green
                'Greedy': '#d62728',   # Dark red 
                'L1 Eq Probs': '#17becf'     # Teal/Cyan
            }
        else:
            colors = {label: plt.get_cmap('tab10')(i) for i, label in enumerate(loss_labels)}

        if with_stddev:
            for i, label in enumerate(loss_labels):
                means, stds = inst_loss[label]
                plt.fill_between(
                    alt_indices,
                    np.array(means),
                    np.array(means) + np.array(stds),
                    alpha=0.1,
                    color=colors[label],
                )
                
            for i, label in enumerate(loss_labels):
                means, stds = inst_loss[label]
                plt.plot(
                    alt_indices,
                    np.array(means) + np.array(stds),
                    color=colors[label],
                    linestyle='--',
                    linewidth=1.25,
                    alpha=0.5 # Less transparent than the fill
                )
        
        # Second loop to plot the means
        for i, label in enumerate(loss_labels):
            means, stds = inst_loss[label]
            print(means, stds)
            plt.plot(alt_indices, means, label=label, color=colors[label])

        if true_prac_losses is not None:
            true_prac_loss = true_prac_losses[instance_name]
            ax.scatter(true_prac_loss[0], true_prac_loss[1], color=colors['Practitioner'], label='Practitioner-Selected Alternate Set')

        if upper_bound[instance_name] is not None:
            ax.axhline(y=float(upper_bound[instance_name]), color='k', linestyle='-', linewidth=2, label='_nolegend_')
            ax.text(alt_indices[-1], float(upper_bound[instance_name]), r'$A = \varnothing$', color='k', fontsize=12, verticalalignment='bottom')
        if lower_bound[instance_name] is not None:
            ax.axhline(y=float(lower_bound[instance_name]), color='k', linestyle='-', linewidth=2, label='_nolegend_')
            ax.text(alt_indices[-1], float(lower_bound[instance_name]), r'$A = N$', color='k', fontsize=12, verticalalignment='bottom')

        ax.set_title(f"{instance_name}, $k={ks[instance_name]}$")
        if i == 0:
            ax.set_ylabel(f"Average {loss_type} Loss")
        if i == num_instances-1:
            ax.legend(fontsize=14)

        xticks = [f"$\\frac{{k}}{{{int(ks[instance_name])//int(x)}}}$" if int(x) != int(ks[instance_name]) else r"$k$" for x in alt_indices]
        ax.set_xticks(alt_indices)
        ax.set_xticklabels(xticks)
        
    fig.text(0.5, 0.01, 'Number of Alternates', ha='center', fontsize=14)
    fig.suptitle(r"$L^1$ Loss Convergence", fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def plot_losses_with_shaded_bands(alt_indices, upper_bound, lower_bound, losses, loss_labels, instance_name, k, filename, true_prac_loss =None, loss_type = 'l1', with_stddev = True):
    plt.figure(figsize=(10, 6))
    alt_indices = [int(x) for x in alt_indices]
    if 'L1 Opt' in loss_labels:
        colors = {
            'L1 Opt': '#A020F0', # purple
            'Binary Opt': '#FFA500',         # Bright orange
            'Practitioner': '#2ca02c',         # Green
            'Greedy': '#d62728',   # Dark red 
            'L1 Eq Probs': '#17becf'     # Teal/Cyan
        }
    else:
        colors = {label: plt.get_cmap('tab10')(i) for i, label in enumerate(loss_labels)}
    if with_stddev:
        for i, label in enumerate(loss_labels):
            means, stds = losses[label]
            plt.fill_between(
                alt_indices,
                np.array(means),
                np.array(means) + np.array(stds),
                alpha=0.1,
                color=colors[label],
            )
            
        for i, label in enumerate(loss_labels):
            means, stds = losses[label]
            plt.plot(
                alt_indices,
                np.array(means) + np.array(stds),
                color=colors[label],
                linestyle='--',
                linewidth=1.25,
                alpha=0.5 # Less transparent than the fill
            )
        
    # Second loop to plot the means
    for i, label in enumerate(loss_labels):
        means, stds = losses[label]
        plt.plot(alt_indices, means, label=label, color=colors[label])

    if true_prac_loss is not None:
        plt.scatter(true_prac_loss[0], true_prac_loss[1], color=colors['Practitioner'], label='Practitioner-Selected Alternate Set')

    if upper_bound is not None:
        plt.axhline(y=upper_bound, color='k', linestyle='-', linewidth=2, label='_nolegend_')
        plt.text(alt_indices[-1], upper_bound, r'$A = \varnothing$', color='k', fontsize=8, verticalalignment='bottom')
    if lower_bound is not None:
        plt.axhline(y=lower_bound, color='k', linestyle='-', linewidth=2, label='_nolegend_')
        plt.text(alt_indices[-1], lower_bound, r'$A = N$', color='k', fontsize=8, verticalalignment='bottom')

    plt.title(f"{instance_name} {loss_type} Losses, $k={k}$")
    plt.xlabel("Number of Alternates")
    plt.ylabel(f"Average {loss_type} Loss")
    plt.legend()
    
    # Modify x ticks to show fraction of k in LaTeX format

    xticks = [f"$\\frac{{k}}{{{int(k)//int(x)}}}$" if int(x) != int(k) else r"$k$" for x in alt_indices]
    plt.xticks(alt_indices, xticks)
    
    plt.savefig(filename, bbox_inches='tight')
    plt.close()


def make_violin_plot(losses, labels, num_test_samples, title, plot_filename):
    type_labels = []
    for label in labels:
        type_labels += [label] * num_test_samples
    data = pd.DataFrame({'Losses': losses, 'Type': type_labels})
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Type', y='Losses', data=data)
    plt.ylim(0, data['Losses'].max() * 1.1)  # Start y-axis at 0 and add some padding at the top
    plt.title(title)
    plt.savefig(plot_filename)
    plt.close()
    
def plot_betas_from_csv(csv_filepath, title, filename):
    labels = []
    betas = []
    with open(csv_filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            feature = row['feature']
            value = row['value']
            labels.append(f"{feature}-{value}")
            betas.append(float(row['beta']))

    plt.figure(figsize=(12, 8))
    plt.bar(labels, betas)
    plt.xlabel('Feature-Value')
    plt.ylabel('Beta')
    plt.title(title)
    plt.ylim(0, 1)  # Set y-axis limits from 0 to 1
    plt.xticks(rotation=45, ha='right')  # Rotate x-tick labels and align them to the right
    plt.tight_layout()  # Adjust layout to make room for the rotated x-tick labels
    plt.savefig(filename)
    plt.close()