# AWS operations

## ALB unhealthy targets
For unhealthy ALB targets, inspect health check paths, target ports, security groups, and application readiness. Confirm the target is in an enabled availability zone. Check target group reason codes and application logs. A successful TCP connection alone does not establish application readiness.

## S3 AccessDenied
When S3 returns AccessDenied, inspect the caller identity, IAM identity policy, bucket policy, service control policies, and permission boundaries. An explicit deny overrides an allow. If SSE-KMS is used, check the KMS key policy and decrypt permissions. Do not fix access failures by making a bucket public.

## CloudWatch alarm investigation
When a CloudWatch alarm fires, identify the metric, dimensions, evaluation window, and recent deployments. Compare error rate, latency, and traffic to the baseline. Validate whether the user-facing service is affected. Record timestamps and mitigation steps in the incident timeline.
