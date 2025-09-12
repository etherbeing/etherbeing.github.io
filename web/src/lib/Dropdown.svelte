<script lang="ts">
    import type { Snippet } from "svelte";
    import { Es, Gb } from "svelte-flag-icons";
    let open = $state(false);
    let hideTimeout = $state<NodeJS.Timeout | undefined>();
    export const {
        options,
        option,
    }: {
        options: { value: string; lang: string }[];
        option: { value: string; lang: string };
        option_icon: Snippet<[{ value: string; lang: string }]>;
        option_label: Snippet<[{ value: string; lang: string }]>;
    } = $props();
</script>

{#snippet option_label(option: { value: string; lang: string })}<span
        >{option.value}</span
    >{/snippet}

{#snippet option_icon(option: { value: string; lang: string })}
    {@render option_label(option)}
{/snippet}

<li
    class="flex flex-col justify-center items-center relative p-0 m-0"
    onmouseenter={() => {
        if (hideTimeout) {
            clearTimeout(hideTimeout);
        }
    }}
    onmouseleave={() => {
        hideTimeout = setTimeout(() => {
            open = false;
            hideTimeout = undefined;
        }, 500);
    }}
>
    <a
        class="nav-link cursor-pointer"
        href={null}
        onclick={(ev) => {
            ev.preventDefault();
            open = !open;
        }}
    >
        <!-- <slot option={options[0]} name="option_icon"></slot> -->
        {@render option_icon(options[0])}
    </a>
    <ul
        class="{open
            ? 'flex'
            : 'hidden'} absolute bg-white mt-3 px-0 mx-0 py-3 gap-1 flex-col text-black rounded-xs w-[200px] shadow-md"
    >
        {#each options as option}
            <li
                class="flex gap-1 justify-between w-full px-3 transition-all hover:bg-gray-200 cursor-pointer py-1"
            >
                {@render option_icon(option)}
                {@render option_label(option)}
            </li>
        {/each}
    </ul>
</li>
