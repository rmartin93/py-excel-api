```tsx
<div className="space-y-4">
	{[1, 2, 3].map((i) => (
		<div key={i} className="flex gap-3 p-3">
			<Skeleton className="h-8 w-8 rounded-full" />
			<div className="flex-1 space-y-2">
				<div className="flex items-center justify-between">
					<Skeleton className="h-4 w-24" />
					<Skeleton className="h-3 w-32" />
				</div>
				<Skeleton className="h-4 w-full" />
				<Skeleton className="h-4 w-3/4" />
			</div>
		</div>
	))}
</div>
```
