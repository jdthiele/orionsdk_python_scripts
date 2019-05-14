def get_node_uris (nodes, swis):
    node_uris = []
    node_nois = [] #noi = net object ID
    for node in nodes:
        # get the entity URI and netOjbId
        uri_query = 'SELECT Caption, NodeID, Uri from Orion.Nodes where Caption=\'' + node + '\''
        results = swis.query(uri_query)
        node_uri = results['results'][0]['Uri']
        node_noi = results['results'][0]['NodeID']
        node_noi = "N:" + str(node_noi)
        node_uris.append(node_uri)
        node_nois.append(node_noi)
    return node_uris, node_nois


def check_nodes (nodes, swis, check_type):
    verified_nodes = []
    for node in nodes:
        # gather mute status
        muted_query = 'SELECT A.ID, N.Caption, A.SuppressFrom, A.SuppressUntil FROM Orion.AlertSuppression A JOIN Orion.Nodes N ON N.Uri = A.EntityUri WHERE N.Caption = \'' + node + '\''
        muted_results = swis.query(muted_query)
        # gather unmanaged status
        unmanaged_query = 'SELECT Caption, UnManageFrom, UnManageUntil FROM Orion.Nodes WHERE Unmanaged = TRUE AND Caption = \'' + node + '\''
        unmanaged_results = swis.query(unmanaged_query)

        # if pre-check and already muted or unmanaged, skip it!
        if check_type == 'pre' and ( muted_results["results"] or unmanaged_results["results"] ):
            print(muted_results["results"])
            print(unmanaged_results["results"])
            print(node + " is already muted muted or unmanaged, skipping")
            continue
        # if post checks, print the respective results for verification of dates
        elif check_type == 'post-mute':
            print(muted_results["results"][0])
        elif check_type == 'post-unmanage':
            print(unmanaged_results["results"][0])
        # else add it to verified hosts for processing
        else:
            verified_nodes.append(node)
    return verified_nodes


def mute_nodes (nodes, swis, startdate, stopdate):
    # precheck nodes to see if they're already muted/unmanaged
    verified_nodes = check_nodes(nodes, swis, 'pre')
    # get node uris
    node_uris, node_nois = get_node_uris(verified_nodes, swis)
    # mute alerts
    print(node_uris)
    results = swis.invoke('Orion.AlertSuppression','SuppressAlerts', node_uris, startdate, stopdate)
    # post check nodes to verify dates
    check_nodes(verified_nodes, swis, 'post-mute')
    return results


def unmanage_nodes (nodes, swis, startdate, stopdate):
    # precheck nodes to see if they're already muted/unmanaged
    verified_nodes = check_nodes(nodes, swis, 'pre')
    # get node uris
    node_uris, node_nois = get_node_uris(verified_nodes, swis)
    # unmanage nodes
    for node_noi in node_nois:
        results = swis.invoke('Orion.Nodes','Unmanage', node_noi, startdate, stopdate, False)
    # post check nodes to verify dates
    check_nodes(verified_nodes, swis, 'post-unmanage')
    return results