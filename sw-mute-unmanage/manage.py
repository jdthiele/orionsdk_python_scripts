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
    return { 'node_uris': node_uris, 'node_nois': node_nois }


def check_nodes (nodes, swis, check_type):
    verified_nodes = []
    for node in nodes:
        # check if node exists in SolarWinds
        uri_query = 'SELECT Caption, NodeID, Uri from Orion.Nodes where Caption=\'' + node + '\''
        uri_results = swis.query(uri_query)
        if len(uri_results['results']) == 0:
            print("Warning: " + node + " does not exist in SolarWinds. skipping")
            continue

        # gather mute status
        muted_query = 'SELECT A.ID, N.Caption, A.SuppressFrom, A.SuppressUntil FROM Orion.AlertSuppression A JOIN Orion.Nodes N ON N.Uri = A.EntityUri WHERE N.Caption = \'' + node + '\''
        muted_results = swis.query(muted_query)
        if len(muted_results["results"]) == 0:
            muted_results = None
        else:
            muted_results = muted_results["results"][0]

        # gather unmanaged status
        unmanaged_query = 'SELECT Caption, UnManageFrom, UnManageUntil FROM Orion.Nodes WHERE Unmanaged = TRUE AND Caption = \'' + node + '\''
        unmanaged_results = swis.query(unmanaged_query)
        if len(unmanaged_results["results"]) == 0:
            unmanaged_results = None
        else:
            unmanaged_results = unmanaged_results["results"][0]

        # if pre-check and already muted or unmanaged, skip it!
        if check_type == 'pre' and ( muted_results or unmanaged_results ):
            if muted_results:
                print(muted_results)
            if unmanaged_results:
                print(unmanaged_results)
            print(node + " is already muted muted or unmanaged, skipping")
            continue
        # if pre-resume and no mutes or umanages in place, skip it!
        elif check_type == 'resume' and muted_results == None and unmanaged_results == None:
            print(node + " is not muted or unmanaged, skipping")
        # if post checks, print the respective results for verification of dates
        elif check_type == 'post-mute':
            if muted_results:
                print(muted_results)
        elif check_type == 'post-unmanage':
            if unmanaged_results:
                print(unmanaged_results)
        elif check_type == 'post-resume':
            verified_nodes.append(node)
        # else add it to verified hosts for processing
        else:
            verified_nodes.append(node)
    return verified_nodes


def mute_nodes (nodes, swis, startdate, stopdate):
    # precheck nodes to see if they're already muted/unmanaged
    verified_nodes = check_nodes(nodes, swis, 'pre')
    # get node uris
    results = get_node_uris(verified_nodes, swis)
    node_uris = results['node_uris']
    # mute alerts
    mute_results = swis.invoke('Orion.AlertSuppression','SuppressAlerts', node_uris, startdate, stopdate)
    # post check nodes to verify dates
    check_nodes(verified_nodes, swis, 'post-mute')
    return mute_results


def unmanage_nodes (nodes, swis, startdate, stopdate):
    # precheck nodes to see if they're already muted/unmanaged
    verified_nodes = check_nodes(nodes, swis, 'pre')
    # get node uris and netObjIds
    results = get_node_uris(verified_nodes, swis)
    node_nois = results['node_nois']
    # unmanage nodes
    unmanage_results = []
    for node_noi in node_nois:
        results = swis.invoke('Orion.Nodes','Unmanage', node_noi, startdate, stopdate, False)
        unmanage_results.append(results)
    # post check nodes to verify dates
    check_nodes(verified_nodes, swis, 'post-unmanage')
    return unmanage_results


def resume_nodes (nodes, swis):
    # precheck nodes to see if they're muted/unmanaged
    verified_nodes = check_nodes(nodes, swis, 'resume')
    # get node uris and netObjIds
    node_uris_nois = get_node_uris(verified_nodes, swis)
    node_uris = node_uris_nois['node_uris']
    node_nois = node_uris_nois['node_nois']
    # unmute nodes
    unmute_results = swis.invoke('Orion.AlertSuppression','ResumeAlerts', node_uris)
    # remanage nodes
    remanage_results = []
    for node_noi in node_nois:
        results = swis.invoke('Orion.Nodes','Remanage', node_noi, False)
        remanage_results.append(results)
    # post check nodes to verify they're not muted or unmanaged anymore
    check_nodes(verified_nodes, swis, 'post-resume')
    return unmute_results, remanage_results