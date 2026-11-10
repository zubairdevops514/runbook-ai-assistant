"""Small, transparent retrieval regression set; not a production benchmark."""
from pathlib import Path
from runbook import Index, load_chunks

CASES = [
    ('pod CrashLoopBackOff previous logs', 'CrashLoopBackOff'),
    ('Pending pods insufficient CPU', 'Pending pods'),
    ('ImagePullBackOff registry credentials', 'ImagePullBackOff'),
    ('ALB unhealthy targets readiness', 'ALB unhealthy targets'),
    ('S3 AccessDenied KMS permissions', 'S3 AccessDenied'),
    ('CloudWatch alarm metric evaluation', 'CloudWatch alarm investigation'),
]


def main():
    index = Index(load_chunks(Path(__file__).parent / 'runbooks'))
    correct = sum(index.search(q, 1)[0]['section'] == expected for q, expected in CASES)
    print(f'Top-1 retrieval accuracy: {correct}/{len(CASES)} on synthetic keyword-oriented queries')
    raise SystemExit(0 if correct == len(CASES) else 1)


if __name__ == '__main__':
    main()
