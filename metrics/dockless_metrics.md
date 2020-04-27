## MDS Dockless Metrics

MDS dockless metrics are a set of defined metrics and compound metrics that are useful for measuring 
dockless vehicle activity with MDS data.  The definitions rely on [MDS core metrics](core_metrics).

The following represents supported MDS dockless metrics extension and definition:

| Metric               | Description                                                                                                          |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| dockless.avg         | Sum of all vehicles in the public right of way.  (vehicles.available.avg + vehicles.unavailable.avg + vehicles.reserved.avg + vehicles.trip.avg) |
| dockless.min         | Sum of all vehicles in the public right of way.  (vehicles.available.min + vehicles.unavailable.min + vehicles.reserved.min + vehicles.trip.min) |
| dockless.max         | Sum of all vehicles in the public right of way.(vehicles.available.max + vehicles.unavailable.max + vehicles.reserved.max +vehicles.trip.max)    |
| dockless.active      | Number of vehicles in PRoW during the interval that had at least one trip during the last x. *Default x = interval*  |
| dockless.inactive    | Number of vehicles in PRoW during the interval that have zero trips during the last x. *Default x = interval*        |
| dockless.utilization | = dockless.active / (dockless.active + dockless.inactive)                                                            |
