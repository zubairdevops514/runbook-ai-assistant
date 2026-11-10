# Kubernetes troubleshooting

## CrashLoopBackOff
A pod in CrashLoopBackOff repeatedly starts and exits. Inspect `kubectl describe pod POD` for events and exit codes. Use `kubectl logs POD --previous` to inspect the last failed container. Check application configuration, missing secrets, and startup probes. Reproduce the failure before changing resource limits. Escalate to the workload owner if logs contain an application exception.

## Pending pods
A Pending pod may be unschedulable because of insufficient CPU or memory, node selectors, taints, or an unbound persistent volume claim. Inspect pod events with `kubectl describe pod POD` and compare resource requests with node allocatable capacity. Confirm the autoscaler has permission and capacity before scaling nodes. Do not remove scheduling constraints without the owner's approval.

## ImagePullBackOff
ImagePullBackOff indicates the container image cannot be pulled. Check the image name, tag, registry availability, and imagePullSecrets. For ECR, confirm node IAM permissions and repository access. Prefer immutable image digests over mutable tags. Do not paste registry credentials into logs or tickets.
