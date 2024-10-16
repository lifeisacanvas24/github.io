<head>
    <meta charset="UTF-8">
    <meta name="description" content="{{ description }}">
    <meta name="keywords" content="{{ keywords | join(', ') }}">
    
    {% for tag in extra %}
    <meta property="og:{{ tag.key }}" content="{{ tag.value }}">
    {% endfor %}
    
    {% for tag in custom.additional_meta_tags %}
    <meta name="{{ tag.name }}" content="{{ tag.content }}">
    {% endfor %}

    <script type="application/ld+json">
    {{ json_ld | json }}
    </script>
</head>
