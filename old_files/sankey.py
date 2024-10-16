import pandas as pd
import plotly.graph_objects as go

pd.set_option('future.no_silent_downcasting', True)

FILENAME = "bio.csv"
def read_csv(FILENAME):
    df = pd.read_csv(FILENAME)
    return df

def code_mapping(df, src, targ):
    """ Map labels in src and targ columns to integers"""
    labels = sorted(set((list(df[src]) + list(df[targ]))))
    codes = range(len(labels))
    lc_map = dict(zip(labels, codes))

    df = df.replace({src: lc_map, targ: lc_map}).infer_objects(copy=False)
    return df, labels
def make_sankey(df, src, targ, *cols, vals=None, **kwargs):
    """
    Create a sankey figure
    df - Dataframe
    src - Source node column
    targ - Target node column
    vals - Linked values (thickness)
    """

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    df, labels = code_mapping(df, src, targ)
    print(df)
    print(labels)

    link = {"source":df[src], "target":df[targ], "value":df[vals]}
    thickness = kwargs.get("thickness", 50)
    pad = kwargs.get("pad", 50)

    node = {"label":labels, "thickness":thickness, "pad":pad}

    sk = go.Sankey(link=link, node=node)

    fig = go.Figure(sk)
    fig.show()

    return fig


# ARGS and KWARGS demonstration
# def add(x, y, *args, msg = "Hello", **kwargs):
#
#     total = x + y
#     for z in args:
#         total += z



def main():
    bio_df = read_csv(FILENAME)
    make_sankey(bio_df, "cancer", "gene", "evidence", thickness = 10, pad = 100)

if __name__ == "__main__":
    main()